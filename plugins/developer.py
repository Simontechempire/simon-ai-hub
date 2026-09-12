from plugins.ai_tools import ask_ai


def explain_code(code: str) -> str:
    return ask_ai(
        f"Explain this code clearly for a beginner:\n\n{code}"
    )


def fix_code(code: str) -> str:
    return ask_ai(
        f"Find bugs in this code and provide a corrected version:\n\n{code}"
    )


def generate_code(request: str) -> str:
    return ask_ai(
        f"Write clean, working code for this request:\n\n{request}"
    )


def review_code(code: str) -> str:
    return ask_ai(
        f"Review this code and suggest improvements:\n\n{code}"
    )
