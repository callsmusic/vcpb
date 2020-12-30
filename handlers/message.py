from pyrogram import filters
from pyrogram.handlers import MessageHandler
from helpers import is_youtube
from ytdl import download
import player
from config import LOG_GROUP
from strings import get_string as _


async def message(client, message):
    if message.text.startswith("/"):
        return

    if not is_youtube(message.text):
        await message.reply_text(_("not_valid"))
        return

    if "list=" in message.text:
        await message.reply_text(_("not_playlist"))
        return

    m = await message.reply_text(_("download_scheduled"), quote=True)

    download(
        (
            m.edit,
            (_("downloading"),)
        ),
        (
            m.edit,
            (_("downloaded_scheduled").format(player.q.qsize() + 1),)
        ),
        [
            player.play,
            [
                None,
                (
                    message.reply_text,
                    (_("playing"),)
                ),
                (
                    message.reply_text,
                    (_("finished_playing"),)
                ),
                None,
                None,
                message.from_user.id,
                message.from_user.first_name,
                [
                    client.send_message,
                    [
                        LOG_GROUP,
                        _("group_log").format(
                            "<a href=\"{}\">{}</a>",
                            "<a href=\"tg://user?id={}\">{}</a>"
                        )
                    ]
                ] if LOG_GROUP else None
            ]
        ],
        (
            m.edit,
            (_("not_live"),)
        ),
        message.text,
        (
            m.edit,
            (_("err_occ"),)
        ),
        [
            m.edit,
            [_("dur_limit"), ]
        ]
    )


__handlers__ = [
    [
        MessageHandler(
            message,
            filters.text
            & filters.private
            & ~ filters.regex(r"^x .+")
        ),
        2
    ]
]
