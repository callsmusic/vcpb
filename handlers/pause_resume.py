from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER


async def pause_resume(client, message):
    if player.pause_resume():
        await message.reply_text("Toggled pause.")
    else:
        await message.reply_text("There's no song playing to pause.")

__handlers__ = [
    [
        MessageHandler(
            pause_resume,
            filters.command("pause", "/")
            & SUDO_FILTER
        )
    ]
]
