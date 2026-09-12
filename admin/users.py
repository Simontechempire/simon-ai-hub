from database import get_user_count


def users_summary():
    count = get_user_count()

    return (
        "👥 USER MANAGEMENT\n\n"
        f"Total registered users: {count}"
    )
