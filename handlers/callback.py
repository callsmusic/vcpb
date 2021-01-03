import subprocess
from asyncio import sleep
from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import player
from helpers import State
from config import SUDO_USERS
from strings import get_string as _


def rm():
    em = "▶️" if player.STATE == State.Paused else "⏸"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄",
                    callback_data="refresh"
                ),
                InlineKeyboardButton(
                    em,
                    callback_data="pause"
                ),
                InlineKeyboardButton(
                    "⏩",
                    callback_data="skip"
                )
            ]
        ]
    )
    return reply_markup


def f10():
    first_10 = player.q_list[:10]
    res = (_("queue_1") + "\n\n").format(
        len(first_10),
        len(player.q_list)
    )

    if first_10:
        for i in range(len(first_10)):
            item = first_10[i]
            res += _("queue_2").format(
                i + 1,
                "<a href=\"{}\">{}</a>".format(
                    item["url"],
                    item["title"]
                ),
                item["dur"],
                "<a href=\"tg://user?id={}\">{}</a>".format(
                    item["sent_by_id"],
                    item["sent_by_name"]
                )
            ) + "\n"
    return res


async def callback(client, query):
    if query.from_user.id not in SUDO_USERS:
        await query.answer()
        return

    if query.data.endswith("volume"):
        current_volume = int(query.message.text.split()[-1].replace("%", ""))

    if query.data == "decrease_volume":
        volume = current_volume - 1

        if volume < 0:
            volume = 0

        volume = f"{volume}%"

        subprocess.Popen(
            ["pactl", "set-sink-volume", "MySink", volume]
        ).wait()

        await query.message.reply_text(
            _("volume_1").format(volume),
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
            ["pactl", "set-sink-volume", "MySink", volume]
        ).wait()

        await query.message.reply_text(
            _("volume_1").format(volume),
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
    else:
        if query.data == "refresh":
            ft = f10()
            mr = rm()
            if query.message.text != ft and query.message.reply_markup != mr:
                await query.message.edit_text(
                    ft,
                    disable_web_page_preview=True,
                    reply_markup=rm()
                )
            await query.answer()
        elif query.data == "skip":
            player.STATE = State.Skipped
            player.abort()
            ft = f10()
            mr = rm()
            if query.message.text != ft and query.message.reply_markup != mr:
                await query.message.edit_text(
                    ft,
                    disable_web_page_preview=True,
                    reply_markup=rm()
                )
            await query.answer()
        elif query.data == "pause":
            if player.STATE == State.Paused:
                player.STATE = State.Playing
            elif player.STATE == State.Playing:
                player.STATE = State.Paused
            player.pause_resume()
            ft = f10()
            mr = rm()
            if query.message.text != ft and query.message.reply_markup != mr:
                await query.message.edit_text(
                    ft,
                    disable_web_page_preview=True,
                    reply_markup=rm()
                )
            await query.answer()


__handlers__ = [
    [
        CallbackQueryHandler(
            callback
        )
    ]
]
