import _thread
import subprocess
from gtts import gTTS
import time
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from strings import get_string as _


async def tts(client, message):
    if message.text.replace("/tts", "") == "":
        await message.reply_text(_("give_text"))
    else:
        try:
            gTTS(message.text.replace("/tts ", ""),
                 lang="en-US").save("downloads/tts.mp3")
            m = await message.reply_text(_("speaking"))
            _thread.start_new_thread(
                subprocess.Popen(["mplayer", "downloads/tts.mp3"]).wait,
                ()
            )
            await m.edit(_("spoke"))
        except:
            await message.reply_text(_("err_occ"))


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
        )
    ],
    [
        MessageHandler(
            x,
            filters.regex(r"^x .+")
        )
    ]
]
