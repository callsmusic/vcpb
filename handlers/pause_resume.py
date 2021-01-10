
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import player
from helpers import State
from config import SUDO_FILTER
from strings import get_string as _


def pause(client, message):
    if player.STATE in State.Playing:
        player.STATE = State.Paused
        player.pause_resume()
        message.reply_text(_("pause_1"))
    elif player.STATE == State.Paused:
        message.reply_text(_("pause_2"))
    else:
        message.reply_text(_("pause_3"))


def resume(client, message):
    if player.STATE == State.Paused:
        player.STATE = State.Playing
        player.pause_resume()
        message.reply_text(_("pause_4"))
    else:
        message.reply_text(_("pause_5"))


__handlers__ = [
    [
        MessageHandler(
            pause,
            filters.command("pause", "/")
            & SUDO_FILTER
        )
    ],
    [
        MessageHandler(
            resume,
            (filters.command("resume", "/")
             | filters.command("play", "/"))
            & SUDO_FILTER
        )
    ]
]
__help__ = {
    "pause": [_("help_pause"), True],
    "resume": [_("help_resume"), True],
    "play": [_("help_play"), True]
}
