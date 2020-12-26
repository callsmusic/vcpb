from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER


async def skip(client, message):
    if player.abort():
        await message.reply_text("Skipped.")
    else:
        await message.reply_text("There's no song playing to be skipped.")

__handlers__ = [
    [
        MessageHandler(
            skip,
            filters.command("skip", "/")
            & SUDO_FILTER
        )
    ]
]
