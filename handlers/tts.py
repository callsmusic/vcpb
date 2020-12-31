import _thread
import subprocess
from gtts import gTTS
import time
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from config import BANNED
from strings import get_string as _


async def tts(client, message):
    if message.text.replace("/tts", "") == "":
        await message.reply_text(_("tts_1"))
    else:
        try:
            gTTS(message.text.replace("/tts ", ""),
                 lang="en-US").save("downloads/tts.mp3")
            m = await message.reply_text(_("tts_2"))
            _thread.start_new_thread(
                subprocess.Popen(["mplayer", "downloads/tts.mp3"]).wait,
                ()
            )
            await m.edit(_("tts_3"))
        except:
            await message.reply_text(_("error"))


async def x(client, message):
    try:
        try:
            await message.delete()
        except:
            pass
        text = message.text.split(" ")
        del text[0]
        text = " ".join(text)
        gTTS(text, lang="en-US").save("downloads/tts.mp3")
        _thread.start_new_thread(
            subprocess.Popen(["mplayer", "downloads/tts.mp3"]).wait,
            ()
        )
    except:
        pass


__handlers__ = [
    [
        MessageHandler(
            tts,
            filters.command("tts", "/")
            & ~ BANNED
        )
    ],
    [
        MessageHandler(
            x,
            filters.regex(r"^x .+")
            & ~ BANNED
        )
    ]
]
__help__ = {
    "tts": [_("help_tts"), False]
}
