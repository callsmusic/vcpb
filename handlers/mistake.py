from pyrogram import Client, filters
from pyrogram.types import Message

from helpers import wrap
from strings import _


@Client.on_message(
    (filters.all & ~ filters.text) & filters.private
)
@wrap
def mistake(client: Client, message: Message):
    message.reply_text(_("mistake"))
