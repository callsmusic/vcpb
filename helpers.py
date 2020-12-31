import os
import re
import pickle
from config import SUDO_USERS

if "data" not in os.listdir():
    open("data", "ab").close()


class State():
    Playing = "PLAYING"
    NothingSpecial = "NOTHING_SPECIAL"
    Paused = "PAUSED"
    Skipped = "SKIPPED"
    Streaming = "STREAMING"


def is_youtube(url):
    exp1 = r"(http|https)\:\/\/(www\.|)youtu\.be\/.+"
    exp2 = r"(http|https)\:\/\/(www\.|)youtube\.com\/watch.+"
    match = bool(re.match(exp1, url)) or bool(re.match(exp2, url))
    return match


def format_dur(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    res = "{}:{}:{}".format(
        hour if len(str(hour)) != 1 else "0" + str(hour),
        minutes if len(str(minutes)) != 1 else "0" + str(minutes),
        seconds if len(str(seconds)) != 1 else "0" + str(seconds)
    )

    return res if not res.startswith("00:") else res[3:]


def get_banned_users():
    f = open("data", "rb")
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


def ban_user(id):
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
    return True


def unban_user(id):
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
