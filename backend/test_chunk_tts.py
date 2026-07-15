import asyncio
import os
from dotenv import load_dotenv
import httpx
import base64

load_dotenv(".env")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
BASE_URL = "https://api.sarvam.ai"

SUPPORTED_LANGUAGES = {
    "en-IN": {
        "name": "English", "native": "English",
        "stt_code": "en-IN",
        "tts_speaker_female": "ritu",
        "tts_speaker_male": "shubh",
    }
}

async def synthesize_speech(
    text: str,
    language: str = "en-IN",
    gender: str = "female",
    emotion: str = "Neutral",
) -> bytes:
    """
    Convert text to speech using Sarvam Bulbul with dynamic emotional parameters.
    """
    lang_config = SUPPORTED_LANGUAGES.get(language, SUPPORTED_LANGUAGES["en-IN"])
    speaker = lang_config["tts_speaker_female"] if gender == "female" else lang_config["tts_speaker_male"]

    # Emotional Mapping for Sarvam Bulbul-v3
    # Pace: 0.5–2.0, Temperature: 0.01–1.0, Pitch: 0.5-2.0
    EMOTION_PARAMS = {
        "Sadness":  {"pace": 1.05, "pitch": 0.95, "temperature": 0.75},
        "Anxiety":  {"pace": 1.15, "pitch": 1.00, "temperature": 0.65},
        "Anger":    {"pace": 1.25, "pitch": 1.05, "temperature": 0.80},
        "Positive": {"pace": 1.20, "pitch": 1.05, "temperature": 0.85},
        "Neutral":  {"pace": 1.18, "pitch": 1.00, "temperature": 0.80},
        "Crisis":   {"pace": 1.10, "pitch": 0.95, "temperature": 0.70},
    }
    params = EMOTION_PARAMS.get(emotion, EMOTION_PARAMS["Neutral"])
    final_pace = max(0.5, min(2.0, params["pace"]))
    final_temp = max(0.01, min(1.0, params["temperature"]))

    # Clean text to prevent robotic pauses (e.g. from markdown or excessive punctuation)
    import re
    text = re.sub(r'[\n\r]+', ' ', text)  # Remove newlines
    text = re.sub(r'\.{2,}', '.', text)   # Replace ... with a single period
    text = re.sub(r'[*_#~`]', '', text)   # Remove markdown artifacts
    text = text.replace('  ', ' ').strip()
    
    if not text:
        return b""

    # Bulbul v3 has a 500 character limit per request. Split text into chunks.
    chunks = []
    current_chunk = ""
    # Split by common sentence terminators but keep the punctuation
    sentences = re.split(r'(?<=[.!?|।])\s+', text)
    for sentence in sentences:
        if not sentence.strip():
            continue
        # If a single sentence is > 400 chars, we must split it by words or commas
        if len(sentence) > 400:
            words = sentence.split(' ')
            for word in words:
                if len(current_chunk) + len(word) + 1 < 450:
                    current_chunk += word + " "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = word + " "
        else:
            if len(current_chunk) + len(sentence) + 1 < 450:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())

    import wave
    import io
    wav_bytes_list = []

    async with httpx.AsyncClient(timeout=30.0) as client:
        for chunk in chunks:
            response = await client.post(
                f"{BASE_URL}/text-to-speech",
                headers={
                    "api-subscription-key": SARVAM_API_KEY,
                    "Content-Type": "application/json",
                },
                json={
                    "inputs": [chunk],
                    "target_language_code": language,
                    "speaker": speaker,
                    "pace": final_pace,
                    "temperature": final_temp,
                    "speech_sample_rate": 22050,
                    "enable_preprocessing": True,
                    "model": "bulbul:v3",
                },
            )

            if response.status_code != 200:
                print(f"[TTS Chunk Error] {response.status_code} — {response.text}")
                continue

            resp_json = response.json()
            audios = resp_json.get("audios", [])
            audio_b64 = audios[0] if audios else resp_json.get("audio")
            
            if audio_b64:
                wav_bytes_list.append(base64.b64decode(audio_b64))

    if not wav_bytes_list:
        raise Exception("TTS failed: No audio generated for any chunks")

    if len(wav_bytes_list) == 1:
        print(f"[TTS] Generated {len(wav_bytes_list[0])} bytes for language={language} using Bulbul v3 (1 chunk)")
        return wav_bytes_list[0]

    # Concatenate WAV files correctly
    out_io = io.BytesIO()
    try:
        with wave.open(out_io, 'wb') as out_wav:
            for i, wb in enumerate(wav_bytes_list):
                try:
                    with wave.open(io.BytesIO(wb), 'rb') as w:
                        if i == 0:
                            out_wav.setparams(w.getparams())
                        out_wav.writeframes(w.readframes(w.getnframes()))
                except Exception as e:
                    print(f"[TTS] Error appending wav chunk: {e}")
        final_wav = out_io.getvalue()
        print(f"[TTS] Generated {len(final_wav)} bytes for language={language} using Bulbul v3 ({len(wav_bytes_list)} chunks)")
        return final_wav
    except Exception as e:
        print(f"[TTS] Error concatenating wavs, returning first chunk: {e}")
        return wav_bytes_list[0]

async def test():
    text = "Hello there. " * 80
    res = await synthesize_speech(text)
    print("SUCCESS", len(res))

asyncio.run(test())
