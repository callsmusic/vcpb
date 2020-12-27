from pyrogram import filters
from pyrogram.handlers import MessageHandler
from helpers import is_youtube
from ytdl import download
import player
from config import LOG_GROUP


async def message(client, message):
    if message.text.startswith("/"):
        return

    if not is_youtube(message.text):
        await message.reply_text("This (link) is not valid.")
        return
    
    if "list=" in message.text:
        await message.reply_text("Send me a video link, not a playlist link.")
        return
    
    await message.reply_text("Download scheduled.", quote=True)
    download(
        (
            message.reply_text,
            ("Downloading...",)
        ),
        (
            message.reply_text,
            (f"Downloaded and scheduled to play at position {player.q.qsize() + 1}.",)
        ),
        [
            player.play,
            [
                None,
                (
                    message.reply_text,
                    ("Playing...",)
                ),
                (
                    message.reply_text,
                    ("Finished playing...",)
                ),
                None,
                None,
                message.from_user.id,
                message.from_user.first_name,
                [
                    client.send_message,
                    [
                        LOG_GROUP,
                        "<b>NOW PLAYING</b>\n"
                        "Title: <a href=\"{}\">{}</a>\n"
                        "Requested By: <a href=\"tg://user?id={}\">{}</a>"
                    ]
                ] if LOG_GROUP else None
            ]
        ],
        message.text,
    )


__handlers__ = [
    [
        MessageHandler(
            message,
            filters.text
            & filters.private
            & ~ filters.regex(r"^x .+")
        ),
        2
    ]
]
