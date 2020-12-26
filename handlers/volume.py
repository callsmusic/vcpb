import subprocess
import re
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import player
from config import SUDO_USERS


async def volume(client, message):
    if len(message.text.split()) == 2:
        try:
            volume = int(message.text.split()[1])
            if volume in range(1, 101):
                volume = f"{volume}%"
                subprocess.Popen(
                    [
                        "pactl",
                        "set-sink-volume",
                        "MySink",
                        volume
                    ]
                ).wait()
                await message.reply_text(
                    f"Volume set to {volume}"
                )
                return
        except:
            pass

    current_volume = "".join(re.search(r"Volume\:(.+)\n", subprocess.check_output(
        ["pactl", "list", "sinks"]).decode()).group(0).split()).split("/")[1]

    if message.from_user.id in SUDO_USERS:
        await message.reply_text(
            f"Current volume is {current_volume}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "➖",
                            callback_data="decrease_volume"
                        ),
                        InlineKeyboardButton(
                            "➕",
                            callback_data="increase_volume"
                        )
                    ]
                ]
            ),
            quote=True
        )
    else:
        await message.reply_text(
            f"Current volume is {current_volume}",
        )

__handlers__ = [
    [
        MessageHandler(
            volume,
            filters.command("volume", "/")
        )
    ]
]
