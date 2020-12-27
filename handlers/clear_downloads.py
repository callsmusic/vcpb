import os
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER


async def clear_downloads(client, message):
    player.abort()
    try:
        for file in os.listdir("downloads"):
            try:
                os.remove("downloads/" + file)
            except:
                pass
        await message.reply_text("Removed all files in your downloads folder.")
    except:
        await message.reply_text("An error occured, your downloads folder might be empty.")

__handlers__ = [
    [
        MessageHandler(
            clear_downloads,
            filters.command("cleardownloads", "/")
            & SUDO_FILTER
        )
    ]
]
