
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
    if not player.mpv.pause:
        player.mpv.pause = True
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
    if player.mpv.pause:
        player.mpv.pause = False
        message.reply_text(_("pause_3"))
    else:
        message.reply_text(_("pause_4"))


@Client.on_message(
    filters.command("skip", "/") & SUDO_FILTER
)
@wrap
def skip(client, message):
    try:
        player.mpv.stop()
        message.reply_text(_("skip_1"))
    except:
        message.reply_text(_("skip_2"))


@Client.on_message(
    filters.command("seekf", "/") & SUDO_FILTER
)
def seekf(client, message):
    if player.mpv.filename or player.mpv.pause:
        try:
            player.mpv.seek(int(message.command[1]))
            message.reply_text(_("seek_1"))
        except:
            message.reply_text(_("seek_2"))
    else:
        message.reply_text(_("seek_3"))


@Client.on_message(
    filters.command("seekb", "/") & SUDO_FILTER
)
def seekb(client, message):
    if player.mpv.filename or player.mpv.pause:
        try:
            player.mpv.seek(-int(message.command[1]))
            message.reply_text(_("seek_1"))
        except:
            message.reply_text(_("seek_2"))
    else:
        message.reply_text(_("seek_3"))


__help__ = {
    "pause": [_("help_pause"), True],
    "resume": [_("help_resume"), True],
    "play": [_("help_play"), True],
    "skip": [_("help_skip"), True],
    "seekf": [_("help_seekf"), True],
    "seekb": [_("help_seekb"), True],
}
