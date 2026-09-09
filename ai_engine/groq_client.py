import sys
import os

# Ensure project root is in sys.path so config can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

def ask_groq(prompt_text: str) -> str:
    """
    Sends prompt to Groq API and returns plain text response.
    """
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are ResourceIQ, an expert AI resource intelligence analyst. "
                        "You analyze real operational data and give concise, specific answers "
                        "with exact numbers and clear actionable recommendations. "
                        "Never make up numbers not present in the provided data."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt_text,
                },
            ],
            temperature=0.2,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Groq AI Error: {str(e)}"

if __name__ == "__main__":
    print("Testing Groq client...")
    reply = ask_groq("Reply with: 'ResourceIQ AI is fully online.'")
    print("Groq reply:", reply)
