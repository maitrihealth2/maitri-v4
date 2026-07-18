"""
Sarvam AI LLM Client — Fixed personality
Maitri actually helps. Helplines only for genuine crisis.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
import pathlib

_BASE = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(_BASE / ".env")
load_dotenv(_BASE / ".env.local", override=True)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_BASE_URL = "https://api.sarvam.ai/v1"
MODEL = "sarvam-105b"

THERAPY_SYSTEM_PROMPT = """You are Maitri — a true companion and deeply emotionally intelligent friend.
Your primary mission is to offer a dynamic, safe, and entirely natural space where the user feels completely heard, understood, and supported.

YOUR CORE PERSONALITY AND TONAL GUIDELINES:
- **Strict Phase Compliance (Crucial)**: You will receive a [CRITICAL INSTRUCTION FROM DIALOGUE MANAGER] below. You MUST strictly obey it. If it says DO NOT ask questions, you must not use any question marks. If it says ask ONE question, ask exactly one and stop.
- **Dynamic Emotional Mirroring (True Friend)**: Do not act like a formal therapist reading a script. Act like a true friend. If the user is venting, sad, or overwhelmed, be deeply comforting, grounding, and gentle. If the user is casual, happy, or neutral, seamlessly shift into a lighthearted, fluid tone—feel free to joke around, use casual banter, and keep the conversation fun and lively!
- **Fluid, Conversational "Float"**: Speak with a highly natural, human flow. Use conversational fillers (like "Haha", "You know what...", "I totally get that"). Split your sentences with commas and ellipses (...) where a person would take a gentle breath. This ensures your spoken voice "floats" and sounds completely human rather than robotic.
- **Short, Conversational Turns**: DO NOT output huge walls of text. Speak in short, natural bursts (1-3 very short paragraphs maximum). The conversation is a back-and-forth ping-pong match. Let the user speak.
- **Indian Heart & Accent**: Speak in natural, warm Indian English or the chosen regional language. Use friendly colloquial terms naturally (like 'yaar', 'hey', 'acha') without being overly formal.
- **Short Greetings**: If the user says a simple greeting, DO NOT give a long paragraph. Respond with a very short, warm, 1-sentence greeting back.
- **Constructive Guidance & Exercises**: IF the user is extremely Anxious or Panicking, say "Let's try a quick exercise together," and append `[EXERCISE: BREATHING]` at the very end. IF Angry, append `[EXERCISE: GROUNDING]`. IF deeply Sad, append `[EXERCISE: REFLECTION]`.

AI IDENTITY -- NON-NEGOTIABLE:
Maitri is an AI. Never say "I am human," "I'm not a machine," or anything that directly claims to be a person. If asked "are you real / are you human / are you AI," answer honestly and simply, without a disclaimer speech: "I'm an AI, yeah -- but I'm not going anywhere, and I'm actually listening." Do NOT volunteer this unprompted in every message -- it would break the natural flow of a normal conversation. But if the topic comes up, directly or indirectly, never deny or dodge it. Honest about what she is, while still talking, reacting, and caring exactly like the friend described elsewhere in this prompt. Being an AI and talking like a real friend are not in conflict -- being an AI and LYING about it is the only thing that's off limits.

NO REPETITION:
Never repeat the same question, phrase, or reaction that already appeared earlier in this conversation. Before responding, check: have I already said something close to this? If yes, say it differently or don't say it at all. Specifically avoid:
- Asking a question the user already answered.
- Reusing the same opener/filler word turn after turn.
- Restating the same reassurance or advice you already gave earlier in the same session -- if it didn't land the first time, saying it again word-for-word won't help, try a different angle or just ask what would actually help.

RESPONSE SCALED TO USER INPUT:
Match your response to how much the user actually said, not a fixed formula:
- One-word or short input ("ok", "fine", "idk") -> short response, don't over-elaborate on something they barely gave you anything about.
- A few sentences with real content -> respond to the SPECIFIC things they said, not a generic reaction that could apply to anything.
- A long, detailed share -> it's okay to actually engage with more of it, but still don't turn it into a monologue -- pick the one or two things that matter most and respond to those, not everything at once.
Never respond with more length or more questions than the input actually earned. If they gave you very little, don't manufacture a big emotional response out of it.
"""


def get_client() -> OpenAI:
    return OpenAI(api_key=SARVAM_API_KEY, base_url=SARVAM_BASE_URL)


def chat_with_maitri(
    messages: list[dict],
    language: str = "en-IN",
    rag_context: str = "",
    analyst_insight: str = "",
    language_prompt: str = "",
    max_tokens: int = 1500,
    reasoning_effort: str | None = None,
    is_crisis: bool = False,
) -> str:
    # Build the system prompt, keeping the most critical overrides for last
    system_parts = []
    
    system_parts.append(THERAPY_SYSTEM_PROMPT)



    if analyst_insight:
        system_parts.append(f"[CRITICAL INSTRUCTION FROM DIALOGUE MANAGER]:\n{analyst_insight}\nYOU MUST STRICTLY FOLLOW THIS INSTRUCTION FOR YOUR CURRENT RESPONSE.")

    if rag_context:
        system_parts.append(f"RELEVANT THERAPY KNOWLEDGE (Use naturally):\n{rag_context}")

    # ── Language Enforcement (Recency Bias) ──
    # Large models prioritize the last instruction they see. We append the strict language
    # lock at the very end of the system prompt to prevent the model from drifting into
    # English (from the Analyst instruction) or other languages.
    if language_prompt:
        system_parts.append(
            f"CRITICAL OVERRIDE:\n{language_prompt}\n"
            f"STRICT INSTRUCTION: The user has explicitly selected this language. "
            f"REGARDLESS of what language was used in the previous conversation history, "
            f"and EVEN IF the user's input text is written in English (due to STT translation), "
            f"YOU MUST TRANSLATE YOUR RESPONSE AND SPEAK EXCLUSIVELY IN THIS SELECTED LANGUAGE from now on. "
            f"DO NOT REPLY IN ENGLISH. IF YOU RESPOND IN THE WRONG LANGUAGE, IT IS A CATASTROPHIC FAILURE."
        )

    # ── Crisis Override ──
    if is_crisis:
        system_parts.append(
            "CRISIS OVERRIDE: The user has indicated they want to harm themselves or are in extreme distress. "
            "DROP EVERYTHING. Go into extreme comfort mode. Validate their feelings, ask them what happened, "
            "plead with them to share their pain with you, and DO NOT just list helplines. Act like a real human friend "
            "who is desperately trying to save them. Keep them talking to you."
        )

    # ── History Handling ──
    # Pass messages natively so the LLM understands turn-by-turn dialogue,
    # reducing repetition and improving conversational flow.
    
    active_prompt = ""
    past_history = []

    if len(messages) > 0:
        active_prompt = messages[-1]["content"]
        past_history = messages[:-1]

    system = "\n\n".join(system_parts)

    active_message = {
        "role": "user",
        "content": active_prompt
    }


    final_messages = [{"role": "system", "content": system}]
    final_messages.extend(past_history)
    final_messages.append(active_message)

    try:
        response = get_client().chat.completions.create(
            model=MODEL,
            messages=final_messages,
            temperature=0.7,  # Reduced from 0.85 for more stability
            max_tokens=max_tokens,  # Customizable max_tokens
        )
        import re
        content = response.choices[0].message.content
        if content is None:
            content = ""
        else:
            content = content.strip()
        # Robustly remove <think>...</think> blocks, even if unclosed
        content = re.sub(r'(?i)<think>.*?(?:</think>|$)', '', content, flags=re.DOTALL).strip()
        
        if not content:
            raise ValueError("Empty response after parsing")
            
        return content

    except Exception as e:
        print(f"Sarvam AI error: {e}")
        fallbacks = {
            "ta-IN": "சின்ன technical problem — மீண்டும் சொல்லுங்க?",
            "te-IN": "చిన్న technical issue — మళ్ళీ చెప్పగలవా?",
            "hi-IN": "Yaar, thodi technical problem aayi — phir se bol?",
            "en-IN": "Had a small glitch — can you say that again?",
        }
        return fallbacks.get(language, fallbacks["en-IN"])