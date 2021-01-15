import os
import re
from pyrogram.errors import exceptions
from PIL import Image, ImageDraw, ImageFont
import pickle
from config import GROUP, USERS_MUST_JOIN

if "data" not in os.listdir():
    open("data", "ab").close()


class State():
    Playing = "PLAYING"
    NothingSpecial = "NOTHING_SPECIAL"
    Paused = "PAUSED"
    Skipped = "SKIPPED"
    Streaming = "STREAMING"


def is_youtube(url):
    exp1 = r"(http|https)\:\/\/((www|m)\.|)youtu\.be\/.+"
    exp2 = r"(http|https)\:\/\/((www|m)\.|)youtube\.com\/watch.+"
    match = bool(re.match(exp1, url)) or bool(re.match(exp2, url))
    return match


def format_dur(seconds: int) -> str:
    """Inputs time in seconds, to get beautified time,
    as string"""
    result = ""
    v_m = 0
    remainder = seconds
    r_ange_s = {
        "d": (24 * 60 * 60),
        "h": (60 * 60),
        "m": 60,
        "s": 1
    }
    for age in r_ange_s:
        divisor = r_ange_s[age]
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f" {v_m}{age} "
    return " ".join(result.split())


chat = None


def wrap(func):
    global chat

    def wrapper(client, message):
        global chat

        if USERS_MUST_JOIN:
            if not chat:
                chat = client.get_chat(GROUP)
            try:
                if chat.get_member(message.from_user.id).status in ("left", "kicked"):
                    return
            except exceptions.bad_request_400.UserNotParticipant:
                return
        return func(client, message)
    return wrapper

def generate_image(
    thumbnail: str, title: str, duration: str, requestor: str
) -> str:
    title, duration, requestor = (title if len(title) <= 35 else (title[:35] + "...")), (duration if len(duration) <= 35 else (duration[:35] + "...")), (requestor if len(requestor) <= 35 else (requestor[:35] + "..."))
    out = thumbnail.split("/")[0] + "/out" + thumbnail.split("/")[1]
    text_ = "\n".join([title, duration, requestor])
    background = Image.open("assets/png/background.png")
    thumbnail = Image.open(thumbnail).resize(background.size)
    text = Image.open("assets/png/text.png")
    thumbnail.paste(background, (0, 0), background)
    thumbnail.paste(text, (0, 0), text)
    font = ImageFont.truetype("assets/ttf/font.ttf", 50)
    image_editable = ImageDraw.Draw(thumbnail)
    image_editable.text((120, 120), text_, (237, 230, 211), font=font)
    thumbnail.save(out, quality=95)
    return out

