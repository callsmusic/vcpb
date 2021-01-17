import subprocess
from pyrogram import Client, filters
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import db
import player
from config import SUDO_FILTER
from strings import get_string as _


@Client.on_callback_query(filters.regex(".+volume") & SUDO_FILTER)
def callback(client, query):
    current_volume = int(query.message.text.split()[-1].replace("%", ""))

    if query.data == "decrease_volume":
        volume = current_volume - 1

        if volume < 0:
            volume = 0

        volume = f"{volume}%"

        subprocess.Popen(["pactl", "set-sink-volume", "MySink", volume]).wait()

        query.message.reply_text(
            _("volume_1").format(volume),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("➖", callback_data="decrease_volume"),
                        InlineKeyboardButton("➕", callback_data="increase_volume"),
                    ]
                ]
            ),
            quote=False,
        )
        query.message.delete()
        query.answer()
    elif query.data == "increase_volume":
        volume = current_volume + 1

        if volume > 100:
            volume = 100

        volume = f"{volume}%"

        subprocess.Popen(["pactl", "set-sink-volume", "MySink", volume]).wait()

        query.message.reply_text(
            _("volume_1").format(volume),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("➖", callback_data="decrease_volume"),
                        InlineKeyboardButton("➕", callback_data="increase_volume"),
                    ]
                ]
            ),
            quote=False,
        )
        query.message.delete()
        query.answer()


@Client.on_callback_query(filters.regex(".+playlist") & SUDO_FILTER)
def playlist(client, query):
    cp = player.currently_playing

    if query.data.startswith("add_to"):
        if db.add_to_playlist(
            cp["file"],
            cp["title"],
            cp["url"],
            cp["sent_by_id"],
            cp["sent_by_name"],
            cp["duration"],
        ):
            query.answer(_("playlist_4"))
        else:
            query.answer(_("playlist_5"))
    elif query.data.startswith("rm_from"):
        if db.remove_from_playlist(cp["url"]):
            query.message.edit_reply_markup(
                InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(_("playlist_3"), "add_to_playlist"),
                            InlineKeyboardButton(_("message_4"), "close"),
                        ],
                    ]
                )
            )
            query.answer(_("playlist_7"))
        else:
            query.answer(_("playlist_8"))


@Client.on_callback_query(filters.regex("close") & SUDO_FILTER)
def close(client, query):
    query.message.delete()
    query.answer()
