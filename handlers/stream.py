from asyncio import sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from helpers import State
from config import SUDO_FILTER, LOG_GROUP
from strings import get_string as _


async def stream(client, message):
    if player.STATE in (State.Playing, State.Paused):
        m = await message.reply_text(
            _("stream_3")
        )
    else:
        args = message.text.split()

        if len(args) == 1:
            m = await message.reply_text(
                _("stream_1")
            )
        elif len(args) != 2:
            m = await message.reply_text(
                _("stream_2")
            )
        else:
            player.stream(
                args[1],
                [
                    client.send_message,
                    [
                        LOG_GROUP,
                        _("group_2").format(
                            args[1]
                        )
                    ]
                ] if LOG_GROUP else None
            )

            await message.reply_text(
                _("stream_4")
            )

    if m and message.chat.type != "private":
        await sleep(5)
        await m.delete()

        try:
            await message.delete()
        except:
            pass

__handlers__ = [
    [
        MessageHandler(
            stream,
            filters.command("stream", "/")
            & SUDO_FILTER
        )
    ]
]
