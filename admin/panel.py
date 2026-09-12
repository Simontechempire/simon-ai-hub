import os

ADMIN_ID = os.getenv("ADMIN_ID")


def is_owner(user_id: int) -> bool:
    return ADMIN_ID and str(user_id) == str(ADMIN_ID)


def admin_panel_text() -> str:
    return (
        "👑 SIMON AI HUB — ADMIN PANEL\n\n"
        "📊 /adminstats — Statistics\n"
        "👥 /users — Users\n"
        "📢 /broadcast — Broadcast\n"
        "🔧 /maintenance — Maintenance\n"
    )
