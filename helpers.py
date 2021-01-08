import os
import re
from pyrogram.errors import exceptions
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
    NoNotifications = "DONT_NOTIFY"


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


def get_banned_users() -> list:
    f = open("data", "rb")
    r = []
    try:
        up = pickle.load(f)
        if "banned_users" in up:
            r = up["banned_users"]
        else:
            r = []
    except:
        pass
    f.close()
    return r


def ban_user(id: int, SUDO_USERS: list) -> bool:
    banned_users = get_banned_users()

    if id in banned_users or id in SUDO_USERS:
        return False

    banned_users.append(id)
    f = open("data", "wb")
    pickle.dump(
        {
            "banned_users": banned_users
        },
        f
    )
    f.close()

    for i in range(len(player.q_list)):
        try:
            if player.q_list[i]["sent_by_id"] == id:
                del player.q_list[i]
        except:
            pass

    return True


def unban_user(id: int) -> bool:
    banned_users = get_banned_users()
    if id not in banned_users:
        return False
    banned_users.remove(id)
    f = open("data", "wb")
    pickle.dump(
        {
            "banned_users": banned_users
        },
        f
    )
    f.close()
    return True


chat = None


def wrap(func):
    global chat

    def wrapper(client, message):
        global chat

        if message.from_user.id in get_banned_users():
            return
        elif USERS_MUST_JOIN:
            if not chat:
                chat = client.get_chat(GROUP)
            try:
                if chat.get_member(message.from_user.id).status in ("left", "kicked"):
                    return
            except exceptions.bad_request_400.UserNotParticipant:
                return
        return func(client, message)
    return wrapper
