from time import sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from helpers import wrap
from config import SUDO_FILTER
from strings import get_string as _


@wrap
async def n4u(client, message):
    m = message.reply_text(_("n4u"))

    if m and message.chat.type != "private":
        sleep(5)
        m.delete()

        try:
            message.delete()
        except:
            pass


__handlers__ = [
    [
        MessageHandler(
            n4u,
            (filters.command("pause", "/")
             | filters.command("skip", "/")
             | filters.command("resume", "/")
             | filters.command("stream", "/")
             | filters.command("bans", "/")
             | filters.command("ban", "/")
             | filters.command("unban", "/")
             | filters.command("cleardownloads", "/")
             | filters.command("play", "/")
             | filters.command("r", "/"))
            & ~ SUDO_FILTER
        )
    ]
]
