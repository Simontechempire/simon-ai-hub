import os
from openai import OpenAI


API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")


client = OpenAI(api_key=API_KEY)


def ask_ai(message: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=message,
    )

    return response.output_text
