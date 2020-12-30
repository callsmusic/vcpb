from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER, LOG_GROUP
from strings import get_string as _


async def stream(client, message):
    if player.q_list:
        await message.reply_text(
            _("cant_stream")
        )
    else:
        args = message.text.split()

        if len(args) == 1:
            await message.reply_text(
                _("url_arg")
            )
        elif len(args) != 2:
            await message.reply_text(
                _("more_than_one_args")
            )
        else:
            stream = player.stream(
                args[1],
                [
                    client.send_message,
                    [
                        LOG_GROUP,
                        _("group_log_stream").format(
                            args[1]
                        )
                    ]
                ] if LOG_GROUP else None
            )

            await message.reply_text(
                _("streaming")
            )

__handlers__ = [
    [
        MessageHandler(
            stream,
            filters.command("stream", "/")
            & SUDO_FILTER
        )
    ]
]
