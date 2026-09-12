from datetime import datetime
import math


def calculator(expression: str):
    allowed = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pi": math.pi,
    }

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            allowed
        )
        return str(result)
    except Exception:
        return "❌ Invalid calculation."


def current_time():
    return datetime.now().strftime("%H:%M:%S")


def current_date():
    return datetime.now().strftime("%Y-%m-%d")
