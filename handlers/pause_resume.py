from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER
from strings import get_string as _


async def pause_resume(client, message):
    if player.pause_resume():
        await message.reply_text(_("paused"))
    else:
        await message.reply_text(_("nothing_playing_pause"))

__handlers__ = [
    [
        MessageHandler(
            pause_resume,
            filters.command("pause", "/")
            & SUDO_FILTER
        )
    ]
]
