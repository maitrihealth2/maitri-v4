import uuid
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.models import get_db, Session as DBSession, Message, MessageEmotion, RiskLog, User
from ai_engine.sarvam_client import chat_with_maitri
from ai_engine.emotion_detector import detect_emotion, detect_emotion_heuristic
from ai_engine.analyst import analyze_context
from ai_engine.voice_client import get_language_prompt
from services.crisis_handler import check_for_crisis
from api.auth import get_current_user
from api.telemetry import broadcast_event

try:
    from rag.retriever import retrieve_context, is_knowledge_base_ready
    RAG_AVAILABLE = is_knowledge_base_ready()
    if RAG_AVAILABLE:
        print("[RAG] Knowledge base loaded")
    else:
        print("[RAG] Not ready — run: python -m knowledge.loader")
except Exception as e:
    print(f"[RAG] Not available: {e}")
    RAG_AVAILABLE = False
    def retrieve_context(query, n_results=3): return ""

router = APIRouter(prefix="/api/consultation", tags=["consultation"])


class StartSessionResponse(BaseModel):
    session_id: str
    message: str


class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str = "en-IN"


class ChatResponse(BaseModel):
    response: str
    is_crisis: bool
    helplines: list[str]
    session_id: str
    emotion: str
    emotion_emoji: str
    emotion_score: float
    rag_used: bool


@router.post("/start", response_model=StartSessionResponse)
def start_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    token = str(uuid.uuid4())
    session = DBSession(user_id=current_user.id, session_token=token, channel="web")
    db.add(session); db.commit(); db.refresh(session)
    return StartSessionResponse(session_id=token, message="Session started.")


@router.post("/message", response_model=ChatResponse)
async def send_message(
    req: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = db.query(DBSession).filter(
        DBSession.session_token == req.session_id,
        DBSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # ── Telemetry: Text Start ──
    asyncio.create_task(broadcast_event("TEXT_START", "Client Keyboard -> FastAPI", {"text": req.message}))

    # ── Crisis first ──────────────────────────────────────────────────────────
    await broadcast_event("CRISIS_CHECK", "Checking for triggers")
    crisis = check_for_crisis(req.message)
    if crisis.is_crisis:
        db.add(RiskLog(session_id=session.id, user_id=current_user.id,
                       trigger_phrase=crisis.trigger_phrase or req.message[:200],
                       system_response="AI intervened with extreme comfort.", helpline_shown=True))
        session.is_crisis_flagged = True
        db.commit()

    # ── Emotion + LLM concurrently ──────────────────────────────────────────
    async def stagger_telemetry():
        await asyncio.sleep(0.5)
        await broadcast_event("RAG_FETCH", "Fetching knowledge")
        await asyncio.sleep(0.5)
        await broadcast_event("MEMORY_FETCH", "Fetching cross-session memory")
        await asyncio.sleep(0.5)
        await broadcast_event("EMOTION_FETCH", "Analyzing tone")
        await asyncio.sleep(0.5)
        await broadcast_event("LLM_START", "Synthesizing Prompt -> LLM")
        
    asyncio.create_task(stagger_telemetry())

    rag_context = retrieve_context(req.message) if RAG_AVAILABLE else ""
    lang_prompt = get_language_prompt(req.language)

    # Fetch last 30 messages for this specific session
    past = db.query(Message).filter(
        Message.session_id == session.id
    ).order_by(Message.created_at.desc()).limit(30).all()
    past.reverse()
    
    history = [{"role": m.role, "content": m.content} for m in past]
    history.append({"role": "user", "content": req.message})

    # ── Sequential Processing: Emotion -> Analyst -> LLM ─────────────────────
    # 1. Get True Emotion from local HuggingFace pipeline
    try:
        emotion = await asyncio.wait_for(detect_emotion(req.message), timeout=2.0)
    except Exception:
        emotion = detect_emotion_heuristic(req.message)

    await broadcast_event("EMOTION_DETECTED", f"Detected: {emotion.label}")

    # 2. Get Dialogue Phase from Analyst
    await broadcast_event("LLM_START", "Analyst Phase Check...")
    analyst_insight = await analyze_context(history, emotion.label, rag_context)

    # 3. Generate response with Maitri
    await broadcast_event("LLM_START", "Maitri Generation...")
    
    ai_response = await asyncio.to_thread(
        chat_with_maitri,
        messages=history,
        language=req.language,
        rag_context=rag_context,
        analyst_insight=analyst_insight,
        language_prompt=lang_prompt,
        is_crisis=crisis.is_crisis,
    )
    
    await broadcast_event("LLM_DONE", "Response generated")

    # ── Save ──────────────────────────────────────────────────────────────────
    user_msg = Message(session_id=session.id, role="user", content=req.message, language=req.language)
    db.add(user_msg)
    db.flush() # get user_msg.id
    
    if emotion and emotion.label:
        db.add(MessageEmotion(message_id=user_msg.id, emotion_label=emotion.label, score=emotion.score))
        
    ai_msg = Message(session_id=session.id, role="assistant", content=ai_response, language=req.language)
    db.add(ai_msg)
    db.commit()

    return ChatResponse(
        response=ai_response, is_crisis=crisis.is_crisis, helplines=crisis.helplines if crisis.is_crisis else [],
        session_id=req.session_id, emotion=emotion.label,
        emotion_emoji=emotion.emoji, emotion_score=emotion.score,
        rag_used=bool(rag_context),
    )


@router.get("/history")
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = db.query(DBSession).filter(
        DBSession.user_id == current_user.id
    ).order_by(DBSession.started_at.desc()).all()
    return [{"session_id": s.session_token, "started_at": s.started_at,
             "ended_at": s.ended_at, "is_crisis_flagged": s.is_crisis_flagged,
             "channel": s.channel} for s in sessions]


@router.get("/{session_id}")
def get_transcript(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from sqlalchemy.orm import joinedload
    session = db.query(DBSession).options(
        joinedload(DBSession.messages).joinedload(Message.emotion)
    ).filter(
        DBSession.session_token == session_id,
        DBSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    # Using the new ORM relationship defined in models.py, we can just access session.messages
    # They are already ordered by created_at natively!
    return {
        "session_id": session_id,
        "started_at": session.started_at,
        "is_crisis_flagged": session.is_crisis_flagged,
        "messages": [{
            "role": m.role, "content": m.content,
            "created_at": m.created_at, "language": m.language,
            "emotion": m.emotion.emotion_label if m.emotion else None, 
            "emotion_score": m.emotion.score if m.emotion else None,
        } for m in session.messages],
    }

@router.get("/dashboard_stats/overview")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from sqlalchemy import func
    from db.models import UserJournal
    
    total_sessions = db.query(func.count(DBSession.id)).filter(DBSession.user_id == current_user.id).scalar() or 0
    journal_entries = db.query(func.count(UserJournal.id)).filter(UserJournal.user_id == current_user.id).scalar() or 0
    mindful_minutes = (total_sessions * 15) + (journal_entries * 5)
    
    latest_emotion = db.query(MessageEmotion).join(MessageEmotion.message).join(Message.session).filter(
        DBSession.user_id == current_user.id,
        Message.role == "user"
    ).order_by(MessageEmotion.created_at.desc()).first()
    
    current_mood = latest_emotion.emotion_label.capitalize() if latest_emotion else "Calm"
    
    mood_emojis = {
        "Joy": "😊", "Calm": "😌", "Sadness": "😔", "Anger": "😠", "Fear": "😨",
        "Disgust": "🤢", "Surprise": "😲", "Neutral": "😐"
    }
    mood_emoji = mood_emojis.get(current_mood, "😌")
    
    return {
        "total_sessions": total_sessions,
        "journal_entries": journal_entries,
        "mindful_minutes": mindful_minutes,
        "current_mood": current_mood,
        "current_mood_emoji": mood_emoji,
        "wellness_streak": min(total_sessions + journal_entries, 12),
        "today_reflection": {
            "quote": "You do not have to be a fire for every mountain blocking you. You could be a water and soft river your way to freedom too.",
            "author": "Nayyirah Waheed",
            "prompt": "Where can you allow yourself to be softer today?"
        }
    }
