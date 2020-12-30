from asyncio import sleep
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
        m = await message.reply_text(_("paused"))
    elif player.STATE == State.Paused:
        m = await message.reply_text(_("cant_pause"))
    else:
        m = await message.reply_text(_("nothing_playing_pause"))

    if m and message.chat.type != "private":
        await sleep(5)
        await m.delete()

        try:
            await message.delete()
        except:
            pass


async def resume(client, message):
    if player.STATE in State.Paused:
        player.STATE = State.Playing
        player.pause_resume()
        m = await message.reply_text(_("resumed"))
    else:
        m = await message.reply_text(_("cant_resume"))

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
