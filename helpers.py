import re


def is_youtube(url):
    exp1 = r"(http|https)\:\/\/(www\.|)youtu\.be\/.+"
    exp2 = r"(http|https)\:\/\/(www\.|)youtube\.com\/watch.+"
    match = bool(re.match(exp1, url)) or bool(re.match(exp2, url))
    return match
