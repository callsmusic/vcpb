from pyrogram import filters
from pyrogram.handlers import MessageHandler
from config import SUDO_FILTER


async def n4u(client, message):
    await message.reply_text("This is not for you.")


__handlers__ = [
    [
        MessageHandler(
            n4u,
            (filters.command("pause", "/")
             | filters.command("skip", "/")
            | filters.command("stream", "/"))
            & (filters.private)
            & ~ SUDO_FILTER
        )
    ]
]
