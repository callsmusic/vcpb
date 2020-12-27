import subprocess
from gtts import gTTS
from pyrogram import filters
from pyrogram.handlers import MessageHandler


async def tts(client, message):
    if message.text.replace("/tts ", "") == "":
        await message.reply_text("Give me some text to speak.")
        return
    else:
        try:
            gTTS(message.text.replace("/tts ", ""),
                 lang="en-GB").save("tts.mp3")
            m = await message.reply_text("Speaking...")
            subprocess.Popen(["mplayer", "tts.mp3"]).wait()
            await m.edit("Spoke.")
        except:
            await message.reply_text("An eror occured.")


__handlers__ = [
    [
        MessageHandler(
            tts,
            filters.command("tts", "/")
        )
    ]
]
