from pyrogram import Client, filters
from pyrogram.types import Message

from vcpb import player
from helpers.filters import sudo_only
from helpers.decorators import errors


@Client.on_message(filters.command("pause") & sudo_only)
@errors
def pause(_, message: Message):
    if player.mpv.pause:
        message.reply_text("<b>❌ Nothing is playing</b>", quote=False)
    else:
        player.mpv.pause = True
        message.reply_text("<b>⏸ Paused</b>", quote=False)


@Client.on_message((filters.command("resume") | filters.command("play")) & sudo_only)
@errors
def resume(_, message: Message):
    if player.mpv.pause:
        player.mpv.pause = False
        message.reply_text("<b>▶️Resumed</b>", quote=False)
    else:
        message.reply_text("<b>❌ Nothing is paused</b>", quote=False)


@Client.on_message(filters.command("skip") & sudo_only)
@errors
def skip(_, message: Message):
    if player.mpv.filename:
        player.mpv.stop()
        message.reply_text("<b>⏩ Skipped the current song</b>", quote=False)
    else:
        message.reply_text("<b>❌ Nothing is playing</b>", quote=False)


@Client.on_message(filters.command("seekf") & sudo_only)
@errors
def seekf(_, message: Message):
    if player.mpv.filename:
        player.mpv.seek(int(message.command[1]))
        message.reply_text(f"<b>⏩ Skipped {message.command[1]} seconds</b>")
    else:
        message.reply_text("<b>❌ Nothing is playing</b>")


@Client.on_message(filters.command("seekb") & sudo_only)
@errors
def seekb(_, message: Message):
    if player.mpv.filename or player.mpv.pause:
        player.mpv.seek(-int(message.command[1]))
        message.reply_text(f"<b>⏪ Reversed {message.command[1]} seconds</b>")
    else:
        message.reply_text("<b>❌ Nothing is playing</b>")
