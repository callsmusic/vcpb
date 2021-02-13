import os

from pyrogram import Client, filters
from pyrogram.types import Message

from config import SUDO_FILTER
from strings import _


@Client.on_message(
    filters.command("cleardownloads", "/") & SUDO_FILTER
)
def clear_downloads(client: Client, message: Message):
    try:
        for file in os.listdir("downloads"):
            try:
                os.remove("downloads/" + file)
            except:
                pass

        message.reply_text(_("cleardownloads"))
    except:
        message.reply_text(_("error"))


__help__ = {
    "cleardownloads": [_("help_cleardownloads"), True]
}
