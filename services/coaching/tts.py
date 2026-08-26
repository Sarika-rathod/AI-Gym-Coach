import os
from io import BytesIO
from groq import Groq


class TextToSpeech:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")

        self.client = Groq(api_key=api_key)

    def speak(self, text):
        cleaned = (text or "").strip()

        if not cleaned:
            return None

        # Keep feedback short for Orpheus
        cleaned = cleaned[:200]

        try:
            response = self.client.audio.speech.create(
                model="canopylabs/orpheus-v1-english",
                voice="troy",
                input=cleaned,
                response_format="wav"
            )

            audio_bytes = response.read()

            if not audio_bytes:
                print("TTS returned empty audio")
                return None

            print(f"TTS generated {len(audio_bytes)} bytes")
            return audio_bytes

        except Exception as e:
            print(f"TTS ERROR: {e}")
            return None