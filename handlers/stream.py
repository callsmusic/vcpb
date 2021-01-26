
from pyrogram import Client, filters
import player
from helpers import func, State
from config import SUDO_FILTER, LOG_GROUP
from strings import get_string as _


@Client.on_message(
    filters.command("stream", "/") & SUDO_FILTER
)
def stream(client, message):
    if player.STATE in (State.Playing, State.Paused):
        message.reply_text(
            _("stream_3")
        )
    else:
        args = message.text.split()

        if len(args) == 1:
            message.reply_text(
                _("stream_1")
            )
        elif len(args) != 2:
            message.reply_text(
                _("stream_2")
            )
        else:
            player.stream(
                args[1],
                func(
                    client.send_message,
                    LOG_GROUP,
                    _("group_2").format(
                        args[1]
                    )
                ) if LOG_GROUP else None
            )

            message.reply_text(
                _("stream_4")
            )


__help__ = {
    "stream": [_("help_stream"), True]
}
