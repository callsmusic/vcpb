import subprocess
from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import player


async def callback(client, query):
    current_volume = int(query.message.text.split()[-1].replace("%", ""))

    if query.data == "decrease_volume":
        volume = current_volume - 1

        if volume < 0:
            volume = 0

        volume = f"{volume}%"

        subprocess.Popen(
            [
                "pactl",
                "set-sink-volume",
                "MySink",
                volume
            ]
        ).wait()

        await query.message.reply_text(
            f"Current volume is {volume}",
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
            quote=False
        )
        await query.message.delete()
        await query.answer()
    elif query.data == "increase_volume":
        volume = current_volume + 1

        if volume > 100:
            volume = 100

        volume = f"{volume}%"

        subprocess.Popen(
            [
                "pactl",
                "set-sink-volume",
                "MySink",
                volume
            ]
        ).wait()

        await query.message.reply_text(
            f"Current volume is {volume}",
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
            quote=False
        )
        await query.message.delete()
        await query.answer()

__handlers__ = [
    [
        CallbackQueryHandler(
            callback
        )
    ]
]
