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
        m = message.reply_text(_("skip_1"))
    else:
        m = message.reply_text(_("skip_2"))

    if m and message.chat.type != "private":
        sleep(5)
        m.delete()

        try:
            message.delete()
        except:
            pass


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
