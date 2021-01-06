from time import sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from helpers import State
from config import SUDO_FILTER
from strings import get_string as _


async def pause(client, message):
    if player.STATE in State.Playing:
        player.STATE = State.Paused
        player.pause_resume()
        m = message.reply_text(_("pause_1"))
    elif player.STATE == State.Paused:
        m = message.reply_text(_("pause_2"))
    else:
        m = message.reply_text(_("pause_3"))

    if m and message.chat.type != "private":
        sleep(5)
        m.delete()

        try:
            message.delete()
        except:
            pass


async def resume(client, message):
    if player.STATE == State.Paused:
        player.STATE = State.Playing
        player.pause_resume()
        m = message.reply_text(_("pause_4"))
    else:
        m = message.reply_text(_("pause_5"))

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
