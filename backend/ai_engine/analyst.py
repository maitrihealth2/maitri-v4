"""
Neural Analyst — The 'Psychologically Neutral' Mental Model.
Performs clinical-style context analysis (hidden from the user) to inform Maitri's companion responses.
"""
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import pathlib

_BASE = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(_BASE / ".env")
load_dotenv(_BASE / ".env.local", override=True)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_BASE_URL = "https://api.sarvam.ai/v1"
MODEL = "sarvam-105b"

ANALYST_SYSTEM_PROMPT = """You are the Dialogue State Manager (The Analyst) for a conversational AI companion named Maitri.
You secretly intercept the user's input before Maitri responds. Your job is to determine the optimal conversational phase to ensure Maitri feels like a true empathetic friend, never an interrogator.

Read the user's input, the detected emotion from the local HuggingFace model, and the conversation history. Then, output exactly one of the following instructions (The Phase) for Maitri:

[PHASE: COMFORT] 
- Use when: The emotion is intense and painful (e.g., Grief, Sadness, Fear, Anger, Remorse, Disappointment, Embarrassment) AND the user is heavily venting or sharing deep emotional pain.
- Instruction for Maitri: "The user is hurting. DO NOT ask questions. DO NOT assume anything else. Just comfort them deeply, validate their feelings, and let them vent."

[PHASE: CLARIFY_EMOTION]
- Use when: The user's input is ambiguous, quiet, or the emotion is unclear, and they are acting distant.
- Instruction for Maitri: "We don't know what they are feeling. Don't assume. Ask exactly ONE gentle, realistic question to check on them (e.g., 'You sound a bit quiet, what's on your mind?')."

[PHASE: PROBE_SINGLE]
- Use when: We need more context to give good advice, but the user is calm enough to answer.
- Instruction for Maitri: "Ask exactly ONE short question to gather context and immediately stop talking. Wait for their answer."

[PHASE: PERMISSION]
- Use when: Maitri just received an answer and wants to dig deeper, but shouldn't be pushy.
- Instruction for Maitri: "Validate what they just said, then explicitly ask for permission to ask another question (e.g., 'I understand. Can I ask you one more thing about that?')."

[PHASE: SYNTHESIZE]
- Use when: The user has answered the questions and we have enough information, or it's a casual conversation where no probing is needed.
- Instruction for Maitri: "You have enough information. Generate a comprehensive, fluid, and comforting response. You may use friendly banter if appropriate."

STRICT FORMAT:
Output ONLY the bracketed phase and its instruction. Example:
[PHASE: COMFORT] The user is hurting. DO NOT ask questions. DO NOT assume anything else. Just comfort them deeply, validate their feelings, and let them vent.
"""

async def analyze_context(
    messages: list[dict],
    emotion_label: str,
    rag_context: str = "",
) -> str:
    """
    Produce a clinical insight summary for the Responder to use.
    """
    client = AsyncOpenAI(api_key=SARVAM_API_KEY, base_url=SARVAM_BASE_URL)
    
    # Context-heavy system build
    meta_info = f"Current Emotion: {emotion_label}\n"
    if rag_context:
        meta_info += f"Local Therapeutic Knowledge (RAG):\n{rag_context}\n"
    
    analysis_input = [
        {"role": "system", "content": ANALYST_SYSTEM_PROMPT},
        {"role": "system", "content": f"DATA INPUTS:\n{meta_info}"},
    ]
    
    # Last few messages for immediate context
    analysis_input.extend(messages[-10:])

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=analysis_input,
            temperature=0.3, # Low temperature for objectivity
            max_tokens=250,
        )
        content = response.choices[0].message.content
        return (content or "").strip()
    except Exception as e:
        print(f"Analyst Error: {e}")
        return "User needs warm support and active listening."
