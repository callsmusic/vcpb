from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from database import playlists as db
import player
from helpers import wrap, func
from config import SUDO_FILTER, LOG_GROUP
from ytdl import download
from strings import _


db.create_playlist("custom")


@Client.on_message(filters.command("play_playlist", "/") & SUDO_FILTER)
@wrap
def play_playlist(client, message):
    playlist = db.get_playlist("custom")["items"]

    if not playlist:
        message.reply_text(_("playlist_1"))
    elif player.is_currently_playing():
        message.reply_text(_("playlist_9"))
    else:
        message.reply_text(_("playlist_2"))

        for item in playlist:
            download(
                item["url"],
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


@Client.on_message(filters.command("clear_playlist", "/") & SUDO_FILTER)
def clear_playlist(client, message):
    if db.reset_playlist("custom", []):
        message.reply_text(_("playlist_10"))
    else:
        message.reply_text(_("playlist_1"))


@Client.on_message(filters.command("playlist", "/") & SUDO_FILTER)
def playlist(client, message):
    all_ = db.get_playlist("custom")["items"]

    if not all_:
        message.reply_text(_("playlist_1"))
        return

    _all = ""

    for i in range(len(all_)):
        _all += str(i + 1) + ". " + \
            all_[i]["title"] + ": " + all_[i]["url"] + "\n"

    if len(_all) < 4096:
        message.reply_text(_all, parse_mode=None,
                           disable_web_page_preview=True)
    else:
        message.reply_text(
            "https://nekobin.com/"
            + requests.post(
                "https://nekobin.com/api/documents", data={"content": _all}
            ).json()["result"]["key"]
        )


@Client.on_callback_query(filters.regex(".+playlist") & SUDO_FILTER)
def playlist_callback(client, query):
    cp = player.currently_playing

    if query.data.startswith("add_to"):
        if db.add_item_to_playlist(
            "custom",
            {
                "url": cp["url"],
                "title": cp["title"]
            }
        ):
            query.message.edit_reply_markup(
                InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                _("playlist_6"), "rm_from_playlist"),
                        ],
                    ]
                )
            )
            query.answer(_("playlist_4"))
        else:
            query.answer(_("playlist_5"))
    elif query.data.startswith("rm_from"):
        if db.remove_item_from_playlist(
            "custom",
            {
                "url": cp["url"],
                "title": cp["title"]
            }
        ):
            query.message.edit_reply_markup(
                InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                _("playlist_3"), "add_to_playlist"),
                        ],
                    ]
                )
            )
            query.answer(_("playlist_7"))
        else:
            query.answer(_("playlist_8"))


__help__ = {
    "play_playlist": [_("help_play_playlist"), True],
    "clear_playlist": [_("help_clear_playlist"), True],
    "playlist": [_("help_playlist"), True]
}
