from time import sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from helpers import State
from config import SUDO_FILTER
from strings import get_string as _


def skip(client, message):
    if player.STATE in (State.Playing, State.Streaming, State.Paused):
        player.STATE = State.Skipped
        player.abort()
        message.reply_text(_("skip_1"))
    else:
        message.reply_text(_("skip_2"))


__handlers__ = [
    [
        MessageHandler(
            skip,
            filters.command("skip", "/")
            & SUDO_FILTER
        )
    ]
]
__help__ = {
    "skip": [_("help_skip"), True]
}
