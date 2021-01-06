from time import sleep
import os
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER
from strings import get_string as _


def clear_downloads(client, message):
    player.abort()
    try:
        for file in os.listdir("downloads"):
            try:
                os.remove("downloads/" + file)
            except:
                pass
        m = message.reply_text(_("cleardownloads"))
    except:
        m = message.reply_text(_("error"))

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
            clear_downloads,
            filters.command("cleardownloads", "/")
            & SUDO_FILTER
        )
    ]
]
__help__ = {
    "cleardownloads": [_("help_cleardownloads"), True]
}
