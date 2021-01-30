
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import player
from helpers import wrap, State
from config import SUDO_FILTER
from strings import _


@Client.on_message(
    filters.command("pause", "/") & SUDO_FILTER
)
@wrap
def pause(client, message):
    if player.pymplayer.pause():
        message.reply_text(_("pause_1"))
    else:
        message.reply_text(_("pause_2"))


@Client.on_message(
    (
        filters.command("resume", "/")
        | filters.command("play", "/")
    ) & SUDO_FILTER
)
@wrap
def resume(client, message):
    if player.pymplayer.resume():
        message.reply_text(_("pause_3"))
    else:
        message.reply_text(_("pause_4"))


@Client.on_message(
    filters.command("skip", "/") & SUDO_FILTER
)
@wrap
def skip(client, message):
    if player.pymplayer.quit():
        message.reply_text(_("skip_1"))
    else:
        message.reply_text(_("skip_2"))


__help__ = {
    "pause": [_("help_pause"), True],
    "resume": [_("help_resume"), True],
    "play": [_("help_play"), True],
    "skip": [_("help_skip"), True]
}
