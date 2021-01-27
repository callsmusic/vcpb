
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from helpers import wrap
from config import SUDO_FILTER
from strings import _


@Client.on_message(
    (
        filters.command("pause", "/")
        | filters.command("skip", "/")
        | filters.command("resume", "/")
        | filters.command("stream", "/")
        | filters.command("cleardownloads", "/")
        | filters.command("play", "/")
        | filters.command("r", "/")
    ) & ~ SUDO_FILTER
)
@wrap
def n4u(client, message):
    message.reply_text(_("n4u"))
