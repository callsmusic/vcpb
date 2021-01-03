from pyrogram import filters
from pyrogram.handlers import MessageHandler
from helpers import is_youtube
from ytdl import download
import player
from config import LOG_GROUP, BANNED
from strings import get_string as _


async def message(client, message):
    if message.text.startswith("/"):
        return

    if not is_youtube(message.text):
        await message.reply_text(_("message_1"))
        return

    if "list=" in message.text:
        await message.reply_text(_("message_2"))
        return

    if player.q_list != 0:
        m = await message.reply_text(_("message_3"), quote=True)

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
                    client.send_message,
                    [
                        LOG_GROUP,
                        _("group_1").format(
                            "<a href=\"{}\">{}</a>",
                            "<a href=\"tg://user?id={}\">{}</a>",
                            "{}"
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


__handlers__ = [
    [
        MessageHandler(
            message,
            filters.text
            & filters.private
            & ~ filters.regex(r"^x .+")
            & ~ BANNED
        ),
        2
    ]
]
