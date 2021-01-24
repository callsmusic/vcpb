from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers import is_youtube
from ytdl import download
import requests
import player
import db
from helpers import wrap, func
from config import SUDO_FILTER, LOG_GROUP, LOG_GROUP_FILTER
from strings import get_string as _


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
        func(
            player.play,
            sent_by_id=message.from_user.id,
            sent_by_name=message.from_user.first_name,
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
            on_skip=func(message.reply_text, _("skip_3"),),
        ),
        func(m.edit, _("ytdl_1")),
        func(m.edit, _("ytdl_2").format(player.q.qsize() + 1)),
        func(m.edit, _("ytdl_3")),
        func(m.edit, _("error")),
        func(m.edit, _("ytdl_4")),
    )


@Client.on_message(filters.command("play_playlist", "/") & SUDO_FILTER & LOG_GROUP_FILTER)
@wrap
def play_playlist(client, message):
    playlist = db.get_playlist()

    if not playlist:
        message.reply_text(_("playlist_1"))
    elif player.is_currently_playing():
        message.reply_text(_("playlist_9"))
    else:
        message.reply_text(_("playlist_2"))

        for item in playlist:
            download(
                item["url"],
                func(
                    player.play,
                    sent_by_id=message.from_user.id,
                    sent_by_name=message.from_user.first_name,
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
                                        _("playlist_6"), "rm_from_playlist"
                                    ),
                                ],
                            ]
                        ),
                    ),
                )
                if LOG_GROUP
                else None,
            )


@Client.on_message(filters.command("clear_playlist", "/") & SUDO_FILTER & LOG_GROUP_FILTER)
def clear_playlist(client, message):
    if db.remove_all():
        message.reply_text(_("playlist_10"))
    else:
        message.reply_text(_("playlist_1"))


@Client.on_message(filters.command("playlist", "/") & SUDO_FILTER & LOG_GROUP_FILTER)
def playlist(client, message):
    all_ = db.get_playlist()

    if not all_:
        message.reply_text(_("playlist_1"))
        return

    _all = ""

    for i in range(len(all_)):
        _all += str(i + 1) + ". " + all_[i]["title"] + ": " + all_[i]["url"] + "\n"

    if len(_all) < 4096:
        message.reply_text(_all, parse_mode=None, disable_web_page_preview=True)
    else:
        message.reply_text(
            "https://nekobin.com/"
            + requests.post(
                "https://nekobin.com/api/documents", data={"content": _all}
            ).json()["result"]["key"]
        )
