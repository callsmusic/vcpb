from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler
from helpers import is_youtube
from ytdl import download
import player
from helpers import wrap
from config import LOG_GROUP
from strings import get_string as _


@Client.on_message(
    filters.text & filters.private & ~ filters.regex(r"^x .+"),
    group=2
)
@wrap
def message(client, message):
    if message.text.startswith("/"):
        return

    if not is_youtube(message.text):
        message.reply_text(_("message_1"))
        return

    if "list=" in message.text:
        message.reply_text(_("message_2"))
        return

    m = message.reply_text(_("message_3"), quote=True)

    download(
        (
            m.edit,
            (_("ytdl_1"),)
        ),
        (
            m.edit,
            (_("ytdl_2").format(player.q.qsize() + 1),)
        ),
        [
            player.play,
            [
                None,
                (
                    message.reply_text,
                    (_("player_1"),)
                ),
                (
                    message.reply_text,
                    (_("player_2"),)
                ),
                None,
                None,
                message.from_user.id,
                message.from_user.first_name,
                [
                    client.send_photo,
                    [
                        LOG_GROUP,
                        None,
                        _("group_1").format(
                            "<a href=\"{}\">{}</a>",
                            "{}",
                            "<a href=\"tg://user?id={}\">{}</a>"
                        ),
                        "",
                        None,
                        None,
                        True,
                        None,
                        None,
                        InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(_("message_4"), "close")
                                ]
                            ]
                        )
                    ]
                ] if LOG_GROUP else None,
                None,
                (
                    message.reply_text,
                    (_("skip_3"),)
                )
            ]
        ],
        (
            m.edit,
            (_("ytdl_3"),)
        ),
        message.text,
        (
            m.edit,
            (_("error"),)
        ),
        [
            m.edit,
            [_("ytdl_4"), ]
        ]
    )
