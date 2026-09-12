def broadcast_message(message: str) -> str:
    if not message.strip():
        return "❌ Broadcast message cannot be empty."

    return (
        "📢 BROADCAST READY\n\n"
        f"Message:\n{message}"
    )
