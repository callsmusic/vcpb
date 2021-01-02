import os
import re
import pickle

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
    return str(int(seconds / 60)) + " min"


def get_banned_users():
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


def ban_user(id, SUDO_USERS):
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
