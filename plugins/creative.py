from plugins.ai_tools import ask_ai


def generate_idea(prompt: str) -> str:
    return ask_ai(
        f"Create a creative idea based on this request:\n{prompt}"
    )


def write_content(prompt: str) -> str:
    return ask_ai(
        f"Create high-quality creative content for this request:\n{prompt}"
    )


def improve_text(text: str) -> str:
    return ask_ai(
        f"Improve and rewrite this text while keeping its meaning:\n{text}"
    )
