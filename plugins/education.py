from plugins.ai_tools import ask_ai


def answer_question(question: str) -> str:
    return ask_ai(
        f"Answer this educational question clearly and accurately:\n{question}"
    )


def explain_topic(topic: str) -> str:
    return ask_ai(
        f"Explain this topic in simple terms with useful examples:\n{topic}"
    )


def create_quiz(topic: str) -> str:
    return ask_ai(
        f"Create a short educational quiz about:\n{topic}"
    )
