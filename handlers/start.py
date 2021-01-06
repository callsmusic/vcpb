from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BANNED
from strings import get_string as _


async def start(client, message):
    await message.reply_text(
        _("start_1"),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                _("start_2"), switch_inline_query_current_chat="")]]
        )
    )

__handlers__ = [
    [
        MessageHandler(
            start,
            filters.command("start", "/")
            & filters.private
            & ~ BANNED
        )
    ]
]
__help__ = {
    "start": [_("help_start"), False]
}
