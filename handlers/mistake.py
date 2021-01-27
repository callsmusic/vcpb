from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from helpers import wrap
from strings import _


@Client.on_message(
    (filters.all & ~ filters.text) & filters.private
)
@wrap
def mistake(client, message):
    message.reply_text(_("mistake"))
