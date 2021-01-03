import os
import re
import pickle
from strings import get_string as _

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


def format_dur(seconds: int) -> str:
    """Inputs time in seconds, to get beautified time,
    as string"""
    result = ""
    v_m = 0
    remainder = seconds
    r_ange_s = {
        _("days"): (24 * 60 * 60),
        _("hours"): (60 * 60),
        _("minutes"): 60,
        _("seconds"): 1
    }
    for age in r_ange_s:
        divisor = r_ange_s[age]
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f"{v_m} {age}"
    return result


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
