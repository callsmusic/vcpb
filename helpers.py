import re


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
