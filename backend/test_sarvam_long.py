import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv(".env")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
BASE_URL = "https://api.sarvam.ai"

async def test_tts():
    long_text = "Hello " * 150
    print("LENGTH:", len(long_text))
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/text-to-speech",
            headers={
                "api-subscription-key": SARVAM_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "inputs": [long_text],
                "target_language_code": "en-IN",
                "speaker": "ritu",
                "model": "bulbul:v3",
            },
        )
        print("STATUS:", response.status_code)
        print("BODY:", response.text[:200])

asyncio.run(test_tts())
