from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import player
from helpers import wrap
from config import SUDO_USERS, SUDO_FILTER
from strings import get_string as _


@wrap
def queue(client, message):
    m = message.reply_text("....", quote=True)
    first_10 = player.q_list[:10]
    res = (_("queue_1") + "\n\n").format(
        len(first_10),
        len(player.q_list)
    )

    if first_10:
        for i in range(len(first_10)):
            item = first_10[i]
            res += _("queue_2").format(
                i + 1,
                "<a href=\"{}\">{}</a>".format(
                    item["url"],
                    item["title"]
                ),
                item["dur"],
                "<a href=\"tg://user?id={}\">{}</a>".format(
                    item["sent_by_id"],
                    item["sent_by_name"]
                )
            ) + "\n"

    if message.from_user.id in SUDO_USERS:
        m.edit_text(
            res,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔄",
                            callback_data="refresh"
                        ),
                        InlineKeyboardButton(
                            "⏸",
                            callback_data="pause"
                        ),
                        InlineKeyboardButton(
                            "⏭",
                            callback_data="skip"
                        )
                    ]
                ]
            )
        )
    else:
        m.edit_text(res, disable_web_page_preview=True)


def rmitem(client, message):
    try:
        del player.q_list[int(message.text.split()[1])]
        message.reply_text(_("queue_3"))
    except:
        pass


__handlers__ = [
    [
        MessageHandler(
            queue,
            filters.command("queue", "/")
        )
    ],
    [
        MessageHandler(
            rmitem,
            filters.command("rmitem", "/")
            & SUDO_FILTER
        )
    ]
]
__help__ = {
    "queue": [_("help_queue"), False]
}
