import asyncio
from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import player
from config import SUDO_USERS
from strings import get_string as _


async def callback(client, query):
    if query.from_user.id not in SUDO_USERS:
        await query.answer()
        return

    current_volume = int(query.message.text.split()[-1].replace("%", ""))

    if query.data == "decrease_volume":
        volume = current_volume - 1

        if volume < 0:
            volume = 0

        volume = f"{volume}%"

        await asyncio.create_subprocess_exec(
            ["pactl", "set-sink-volume", "MySink", volume]
        ).wait()

        await query.message.reply_text(
            _("current_volume").format(volume),
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

        await asyncio.create_subprocess_exec(
            ["pactl", "set-sink-volume", "MySink", volume]
        ).wait()

        await query.message.reply_text(
            _("current_volume").format(volume),
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
