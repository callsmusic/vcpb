
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import player
from helpers import State
from config import SUDO_FILTER
from strings import get_string as _


@Client.on_message(
    filters.command("skip", "/") & SUDO_FILTER
)
def skip(client, message):
    if player.STATE in (State.Playing, State.Streaming, State.Paused):
        player.STATE = State.Skipped
        player.abort()
        message.reply_text(_("skip_1"))
    else:
        message.reply_text(_("skip_2"))


__help__ = {
    "skip": [_("help_skip"), True]
}
