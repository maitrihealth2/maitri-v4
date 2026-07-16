import re
import os
import httpx
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv
import pathlib
from transformers import pipeline

_BASE = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(_BASE / ".env")
load_dotenv(_BASE / ".env.local", override=True)
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN")
HF_MODEL = "SamLowe/roberta-base-go_emotions"
HF_API_DISABLED = False

_emotion_pipeline = None

def get_emotion_pipeline():
    global _emotion_pipeline
    if _emotion_pipeline is None:
        try:
            print(f"[HF Emotion] Loading local transformers pipeline for {HF_MODEL}...")
            # top_k=1 returns [[{'label': '...', 'score': ...}]] format in recent versions, 
            # or [{'label': '...', 'score': ...}] depending on version. We'll handle both.
            _emotion_pipeline = pipeline("text-classification", model=HF_MODEL, top_k=1)
        except Exception as e:
            print(f"[HF Emotion] Error loading pipeline: {e}")
            _emotion_pipeline = "FAILED"
    return _emotion_pipeline

EMOTION_KEYWORDS = {
    "Anger": [
        "angry", "anger", "furious", "mad", "annoyed", "pissed", "hate", "irritated", "frustrated",
        "gussa", "chidh", "naraz", "kopam", "kopamga", "frustration", "rage", "irritating", 
        "fuming", "outraged", "annoy", "nonsense", "hate this", "screwing", "fed up", 
        "pissing me off", "gusse", "krodh", "dimag kharab", "gussa aa raha", "aag babula", 
        "naaraaz", "kovam", "erichal", "kovama", "veruppu", "kadupu", "kaduppu", "asahanam", 
        "chiraaku", "chiraku", "krodham"
    ],
    "Anxiety": [
        "anxious", "scared", "fear", "worried", "nervous", "panic", "stress", "tense", "stressed",
        "darr", "chinta", "fikr", "dar", "bayama", "bhayama", "tension", "shaking", "restless", 
        "dread", "uneasy", "overthinking", "nervousness", "stressing", "heart racing", "worries", 
        "paranoid", "anxiety", "gabrahat", "ghabrahat", "dara hua", "bechaini", "bechain", "bayam", 
        "padhabadhapu", "kavalai", "acham", "dhik dhik", "bhyama", "bhayam", "kangaaru", "kangaru", 
        "andholana", "andolana"
    ],
    "Sadness": [
        "sad", "depressed", "unhappy", "cry", "lonely", "hopeless", "hurt", "pain", "crying",
        "udaas", "udas", "dukh", "rona", "akela", "sonthama", "badhava", "sadness", "miserable", 
        "heartbroken", "down", "grief", "gloomy", "heavy heart", "weeping", "loneliness", "empty", 
        "shattered", "tear", "tears", "dukhi", "ro raha", "akelapan", "mayus", "gam", "dard", 
        "sogam", "sogama", "soham", "azhugai", "varutham", "thunbam", "thuyaram", "thaniya", 
        "thanimai", "badha", "badhaga", "dhaanyamu", "yedupu", "edupu", "ontarithanam", "ontari", 
        "nirasah", "nirasa"
    ],
    "Positive": [
        "happy", "good", "great", "joy", "excited", "love", "blessed", "wonderful", "cool",
        "khush", "acha", "badhiya", "santhosham", "bagundi", "awesome", "joyful", "glad", 
        "cheerful", "delighted", "amazing", "fantastic", "peaceful", "calm", "satisfied", 
        "proud", "love it", "achha", "maza", "maaza", "sundar", "anand", "anandit", "magizhchi", 
        "nalla", "nalladhu", "arputham", "anbu", "nimmadhi", "santhoshama", "santosham", 
        "chala bagundi", "aanandam", "prashantham", "prasantam", "manchiga", "santhoshanga"
    ],
}

EMOTION_EMOJI = {
    "Anger":    "😤",
    "Anxiety":  "😰",
    "Sadness":  "😔",
    "Positive": "😊",
    "Neutral":  "😐",
    "Crisis":   "🚨",
}

# Mapping GoEmotions (28 labels) to our 6 core UI categories
GO_EMOTIONS_MAP = {
    "admiration": "Positive", "amusement": "Positive", "approval": "Positive", "gratitude": "Positive",
    "joy": "Positive", "love": "Positive", "optimism": "Positive", "pride": "Positive", "relief": "Positive",
    "excitement": "Positive", "pride": "Positive",
    "anger": "Anger", "annoyance": "Anger", "disapproval": "Anger",
    "fear": "Anxiety", "nervousness": "Anxiety",
    "sadness": "Sadness", "disappointment": "Sadness", "grief": "Sadness", "remorse": "Sadness",
    "embarrassment": "Anxiety", "confusion": "Anxiety",
    "desire": "Positive", "curiosity": "Neutral", "surprise": "Neutral",
    "neutral": "Neutral", "caring": "Positive"
}

@dataclass
class EmotionResult:
    label: str          # e.g. "Anxiety"
    emoji: str          # e.g. "😰"
    score: float        # confidence
    raw_label: str      # internal label

def detect_emotion_heuristic(text: str) -> EmotionResult:
    """Keyword-based fallback for low latency."""
    lower = text.lower().strip()
    counts = {label: 0 for label in EMOTION_KEYWORDS.keys()}
    for label, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", lower):
                counts[label] += 1
    
    best_label = "Neutral"
    max_count = 0
    for label, count in counts.items():
        if count > max_count:
            max_count = count; best_label = label
            
    score = min(max_count * 0.4 + 0.5, 1.0) if max_count > 0 else 0.0
    return EmotionResult(best_label, EMOTION_EMOJI.get(best_label, "😐"), score, best_label.lower())


async def detect_emotion(text: str) -> EmotionResult:
    global HF_API_DISABLED
    """
    Main entry point — Deep Learning with Keyword Fallback.
    """
    if not text.strip():
        return EmotionResult("Neutral", "😐", 0.0, "neutral")

    # If no token or if API previously failed, use heuristic immediately
    if not HF_TOKEN or HF_API_DISABLED:
        return detect_emotion_heuristic(text)

    try:
        # Use local transformers pipeline
        pipe = get_emotion_pipeline()
        
        if pipe and pipe != "FAILED":
            # Run the heavy inference in a background thread to prevent blocking asyncio loop
            results = await asyncio.to_thread(pipe, text)
            
            if results:
                # pipeline(top_k=1) returns either a list of lists (batch) or a list of dicts.
                if isinstance(results, list) and isinstance(results[0], list):
                    top_match = results[0][0]
                elif isinstance(results, list) and isinstance(results[0], dict):
                    top_match = results[0]
                else:
                    top_match = None
                    
                if top_match:
                    hf_label = top_match["label"]
                    score = top_match["score"]
                    
                    category = GO_EMOTIONS_MAP.get(hf_label, "Neutral")
                    print(f"[Local HF Emotion] Detected '{hf_label}' -> '{category}' ({score:.2f})")
                    
                    return EmotionResult(
                        label=category,
                        emoji=EMOTION_EMOJI.get(category, "😐"),
                        score=float(score),
                        raw_label=hf_label
                    )
    except Exception as e:
        print(f"[Local HF Emotion] Unexpected error: {e}, falling back.")
        
    return detect_emotion_heuristic(text)

if __name__ == "__main__":
    # Test cases
    tests = [
        "I am so stressed about my exams",
        "I feel lonely and sad",
        "Mujhe bahut gussa aa raha hai",
        "I had a great day!",
        "Normal sentence here.",
    ]
    print("Testing locally...")
    for t in tests:
        # Note: Local test needs to run loop
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(detect_emotion(t))
        print(f"{res.emoji} {res.label:8} | {t}")
