from re import match


def is_youtube(url):
    return bool(match(r"(http|https)\:\/\/((www|m)\.|)youtu\.be\/.+", url)) or \
           bool(match(r"(http|https)\:\/\/((www|m)\.|)youtube\.com\/watch.+", url))
