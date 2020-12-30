from asyncio import sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER
from strings import get_string as _


async def skip(client, message):
    if player.abort():
        m = await message.reply_text(_("skipped"))
    else:
        m = await message.reply_text(_("nothing_playing_skip"))

    if m and message.chat.type != "private":
        await sleep(5)
        await m.delete()

        try:
            await message.delete()
        except:
            pass

__handlers__ = [
    [
        MessageHandler(
            skip,
            filters.command("skip", "/")
            & SUDO_FILTER
        )
    ]
]
