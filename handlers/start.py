from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers import wrap
from strings import get_string as _


@Client.on_message(
    filters.command("start", "/") & filters.private
)
@wrap
def start(client, message):
    message.reply_text(
        _("start_1"),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                _("start_2"), switch_inline_query_current_chat="")]]
        )
    )


__help__ = {
    "start": [_("help_start"), False]
}
