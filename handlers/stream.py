from pyrogram import Client, filters
from pyrogram.types import Message

from vcpb import ytdl, player

from helpers.filters import sudo_only
from helpers.decorators import errors


@Client.on_message(filters.command("stream") & sudo_only)
@errors
def stream(_, message: Message):
    if len(message.command) != 2:
        message.reply_text("<b>❌ 1 argument is required</b>", quote=False)
        return
    elif player.is_streaming():
        message.reply_text("<b>❌ Already streaming</b>", quote=False)
        return

    if not player.queue.empty():
        with player.queue.mutex:
            player.queue.queue.clear()

    if not ytdl.queue.empty():
        with ytdl.queue.mutex:
            ytdl.queue.queue.clear()

    player.stream(message.command[1])
    message.reply_text("<b>📻 Streaming...</b>", quote=False)


@Client.on_message(filters.command("stop") & sudo_only)
@errors
def stop(_, message: Message):
    if not player.is_streaming():
        message.reply_text("<b>❌ Not streaming</b>", quote=False)
        return

    player.stop_streaming()
    message.reply_text("<b>✅ Stopped streaming</b>", quote=False)
