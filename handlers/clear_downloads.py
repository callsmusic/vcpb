
import os
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER
from strings import _


@Client.on_message(
    filters.command("cleardownloads", "/") & SUDO_FILTER
)
def clear_downloads(client, message):
    try:
        for file in os.listdir("downloads"):
            try:
                os.remove("downloads/" + file)
            except:
                pass

        message.reply_text(_("cleardownloads"))
    except:
        message.reply_text(_("error"))


__handlers__ = [
    [
        MessageHandler(
            clear_downloads,
            filters.command("cleardownloads", "/")
            & SUDO_FILTER
        )
    ]
]
__help__ = {
    "cleardownloads": [_("help_cleardownloads"), True]
}
