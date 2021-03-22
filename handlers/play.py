from pyrogram import Client, filters
from pyrogram.types import Message

from vcpb import ytdl, player

from helpers.regex import is_youtube
from helpers.queues import func
from helpers.decorators import errors

from config import CHAT_ID


@Client.on_message(filters.text & filters.private)
@errors
def play(client: Client, message: Message):
    if not is_youtube(message.text):
        return
    elif "list=" in message.text:
        message.reply_text("<b>❌ Can’t play playlists</b>", quote=True)
        return
    elif player.is_streaming():
        message.reply_text("<b>❌ Can’t play while streaming</b>", quote=True)
        return

    m = message.reply_text("<b>✅ Download scheduled</b>", quote=True)

    ytdl.download(
        video=message.text,
        sender_id=message.from_user.id,
        sender_name=message.from_user.first_name,
        play_function=func(
            player.play,
            log=func(
                client.send_message,
                CHAT_ID,
                "<b>▶️ Playing</b> {}\n<b>🕔 Duration:</b> {}\n<b>👤 Requester:</b> {}".format(
                    '<a href="{}">{}</a>',
                    "{}",
                    message.from_user.mention(),
                ),
                disable_web_page_preview=True
            ),
            on_start=func(message.reply_text, "<b>▶️ Playing...</b>", ),
            on_end=func(message.reply_text, "<b>✅ Finished playing</b>", ),
        ),
        on_start=func(m.edit, "<b>🔄 Downloading...</b>"),
        on_end=func(m.edit, "<b>#️⃣ Scheduled to play at position {}</b>".format(player.queue.qsize() + 1)),
        on_is_live_error=func(m.edit, "<b>❌ Can’t download live video</b>"),
        on_error=func(m.edit, "{}: {}"),
    )
