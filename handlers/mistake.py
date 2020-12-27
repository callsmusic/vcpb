from pyrogram import filters
from pyrogram.handlers import MessageHandler
from strings import get_string as _

async def mistake(client, message):
    await message.reply_text(_("mistake"))


__handlers__ = [
    [
        MessageHandler(
            mistake,
            (filters.all & ~ filters.text)
            & filters.private
        )
    ]
]
