from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from helpers import wrap
from strings import get_string as _


@wrap
def mistake(client, message):
    message.reply_text(_("mistake"))


__handlers__ = [
    [
        MessageHandler(
            mistake,
            (filters.all & ~ filters.text)
            & filters.private
        )
    ]
]
