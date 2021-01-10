
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from helpers import wrap
from config import SUDO_FILTER
from strings import get_string as _


@wrap
def n4u(client, message):
    message.reply_text(_("n4u"))


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
