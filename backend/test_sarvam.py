import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv(".env")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
BASE_URL = "https://api.sarvam.ai"

async def test_tts():
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/text-to-speech",
            headers={
                "api-subscription-key": SARVAM_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "inputs": ["Hello world"],
                "target_language_code": "en-IN",
                "speaker": "ritu",
                "pace": 1.18,
                "temperature": 0.8,
                "speech_sample_rate": 22050,
                "enable_preprocessing": True,
                "model": "bulbul:v3",
            },
        )
        print("WITH PACE/TEMP", response.status_code, response.text[:200])

        response2 = await client.post(
            f"{BASE_URL}/text-to-speech",
            headers={
                "api-subscription-key": SARVAM_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "inputs": ["Hello world"],
                "target_language_code": "en-IN",
                "speaker": "ritu",
                "model": "bulbul:v3",
            },
        )
        print("WITHOUT PACE/TEMP", response2.status_code, response2.text[:200])

asyncio.run(test_tts())
