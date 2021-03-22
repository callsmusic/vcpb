from typing import Callable

from pyrogram.types import Message


def errors(func: Callable) -> Callable:
    def decorator(_, message: Message):
        try:
            func(_, message)
        except Exception as e:
            message.reply_text(f"{type(e).__name__}: {e}")
    return decorator
