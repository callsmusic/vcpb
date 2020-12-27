from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER, LOG_GROUP


async def stream(client, message):
    if player.current:
        await message.reply_text(
            "Can't stream while music is playing."
        )
    else:
        args = message.text.split()

        if len(args) == 1:
            await message.reply_text(
                "Give me a stream URL as an arg."
            )
        elif len(args) != 2:
            await message.reply_text(
                "You provided more than an arg."
            )
        else:
            stream = player.stream(
                args[1],
                [
                    client.send_message,
                    [
                        LOG_GROUP,
                        "<b>NOW STREAMING</b>\n"
                        "<pre>{}</pre>".format(
                            args[1]
                        )
                    ]
                ] if LOG_GROUP else None
            )
            if stream == 0:
                await message.reply_text(
                    "Streaming..."
                )

__handlers__ = [
    [
        MessageHandler(
            stream,
            filters.command("stream", "/")
            & SUDO_FILTER
        )
    ]
]
