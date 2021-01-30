from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers import is_youtube
from ytdl import download
import requests
import player
from helpers import wrap, func
from config import SUDO_FILTER, LOG_GROUP
from strings import _


@Client.on_message(
    filters.text & filters.private & ~filters.regex(r"^x .+"), group=2
)
@wrap
def message(client, message):
    if message.text.startswith("/"):
        return

    if not is_youtube(message.text):
        message.reply_text(_("play_1"))
        return

    if "list=" in message.text:
        message.reply_text(_("play_2"))
        return

    m = message.reply_text(_("play_3"), quote=True)

    download(
        message.text,
        message.from_user.id,
        message.from_user.first_name,
        func(
            player.play,
            log=func(
                client.send_photo,
                chat_id=LOG_GROUP,
                caption=_("group_1").format(
                    '<a href="{}">{}</a>',
                    "{}",
                    '<a href="tg://user?id={}">{}</a>',
                ),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                _("playlist_3"), "add_to_playlist"
                            ),
                        ],
                    ]
                ),
            )
            if LOG_GROUP
            else None,
            on_start=func(message.reply_text, _("player_1"),),
            on_end=func(message.reply_text, _("player_2"),),
        ),
        func(m.edit, _("ytdl_1")),
        func(m.edit, _("ytdl_2").format(player.queue.qsize() + 1)),
        func(m.edit, _("ytdl_3")),
        func(m.edit, _("error")),
        func(m.edit, _("ytdl_4")),
    )
