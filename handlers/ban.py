from time import sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from helpers import ban_user, unban_user, get_banned_users
from config import SUDO_FILTER, SUDO_USERS
from strings import get_string as _


def ban(client, message):
    user = message.text.split()

    if len(user) != 2:
        m = message.reply_text(_("ban_1"))
        return

    user = user[1]

    try:
        user = int(user)
        res = ban_user(user, SUDO_USERS)

        if res:
            m = message.reply_text(_("ban_2"))
        else:
            m = message.reply_text(_("ban_3"))
    except:
        m = message.reply_text(_("ban_4"))

    if m and message.chat.type != "private":
        sleep(5)
        m.delete()

        try:
            message.delete()
        except:
            pass


def unban(client, message):
    user = message.text.split()

    if len(user) != 2:
        m = message.reply_text(_("ban_1"))
        return

    user = user[1]

    try:
        user = int(user)
        res = unban_user(user)

        if res:
            m = message.reply_text(_("ban_5"))
        else:
            m = message.reply_text(_("ban_6"))
    except:
        m = message.reply_text(_("ban_4"))

    if m and message.chat.type != "private":
        sleep(5)
        m.delete()

        try:
            message.delete()
        except:
            pass


def bans(client, message):
    banned_users = get_banned_users()
    res = ""

    if not banned_users:
        res = _("ban_7")
    else:
        res = _("ban_8") + "\n"
        for banned_user in banned_users:
            res += "    - `" + str(banned_user) + "`\n"

    m = message.reply_text(res)

    if m and message.chat.type != "private":
        sleep(10)
        m.delete()

        try:
            message.delete()
        except:
            pass


__handlers__ = [
    [
        MessageHandler(
            ban,
            filters.command("ban", "/")
            & SUDO_FILTER
        )
    ],
    [
        MessageHandler(
            unban,
            filters.command("unban", "/")
            & SUDO_FILTER
        )
    ],
    [
        MessageHandler(
            bans,
            filters.command("bans", "/")
            & SUDO_FILTER
        )
    ]
]
__help__ = {
    "ban": [_("help_ban"), True],
    "unban": [_("help_unban"), True],
    "bans": [_("help_bans"), True]
}
