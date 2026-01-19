import requests
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

HF_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

GROQ_API_KEY = os.getenv("GROQ_API")
HF_API_KEY = os.getenv("HF_API")

groqclient = Groq(api_key=GROQ_API_KEY)

system_prompt = "you are a helpful ai assistant"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# ---------------- CHAT ----------------

def build_message_history(chat_history: list):
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    return messages


def chat_with_ai(chat_history: list):
    messages = build_message_history(chat_history)

    response = groqclient.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_completion_tokens=2048,
        top_p=1
    )

    return response.choices[0].message.content


# ---------------- IMAGE ----------------

def generate_image(prompt: str) -> bytes:
    res = requests.post(
        HF_URL,
        headers=headers,
        json={
            "inputs": prompt,
            "options": {"wait_for_model": True}
        },
        timeout=120
    )

    if "image" in res.headers.get("content-type", ""):
        return res.content
    else:
        raise Exception("Image generation failed")
