from pyrogram import filters
from pyrogram.handlers import MessageHandler
from strings import get_string as _
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start(client, message):
    await message.reply_text(
        _("start_1", True),
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
        )
    ]
]
