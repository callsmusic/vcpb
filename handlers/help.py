from pyrogram import Client, filters
from pyrogram.types import Message

from handlers import all_help
from helpers import wrap
from config import SUDO_USERS
from strings import _


def user():
    res = ""

    for help in all_help:
        for h in help:
            if not help[h][1]:
                res += "/" + h + ": " + help[h][0] + "\n"

    return res


def admin():
    res = ""

    for help in all_help:
        for h in help:
            if help[h][1]:
                res += "/" + h + ": " + help[h][0] + "\n"

    return res


@Client.on_message(
    filters.command("help", "/") & filters.private
)
@wrap
def help(client: Client, message: Message):
    message.reply_text("**" + _("help_1") + "**" + "\n" + user() + "\n" + "**" + _(
        "help_2") + "**" + "\n" + admin() if message.from_user.id in SUDO_USERS else user())


__help__ = {
    "help": [_("help_help"), False]
}
