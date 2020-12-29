from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER
from strings import get_string as _


async def skip(client, message):
    if player.abort():
        await message.reply_text(_("skipped"))
    else:
        await message.reply_text(_("nothing_playing_skip"))

__handlers__ = [
    [
        MessageHandler(
            skip,
            filters.command("skip", "/")
            & SUDO_FILTER
        )
    ]
]
