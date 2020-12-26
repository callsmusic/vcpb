from pyrogram import filters
from pyrogram.handlers import MessageHandler


async def start(client, message):
    await message.reply_text("Hi, send me a YouTube link to play it.")

__handlers__ = [
    [
        MessageHandler(
            start,
            filters.command("start", "/")
            & filters.private
        )
    ]
]
