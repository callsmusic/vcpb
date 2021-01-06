import _thread
import subprocess
from gtts import gTTS
import time
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from helpers import wrap
from strings import get_string as _


@wrap
async def tts(client, message):
    if message.text.replace("/tts", "") == "":
        message.reply_text(_("tts_1"))
    else:
        try:
            gTTS(message.text.replace("/tts ", ""),
                 lang="en-US").save("downloads/tts.mp3")
            m = message.reply_text(_("tts_2"))
            _thread.start_new_thread(
                subprocess.Popen(["mplayer", "downloads/tts.mp3"]).wait,
                ()
            )
            m.edit(_("tts_3"))
        except:
            message.reply_text(_("error"))


async def x(client, message):
    try:
        try:
            message.delete()
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
__help__ = {
    "tts": [_("help_tts"), False]
}
