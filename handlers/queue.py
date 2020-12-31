from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import player
from config import SUDO_USERS, SUDO_FILTER
from strings import get_string as _


async def queue(client, message):
    m = await message.reply_text("....")
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
                "<a href=\"{}\">{}</a> ({})".format(
                    item["url"],
                    item["title"],
                    item["dur"]
                ),
                "<a href=\"tg://user?id={}\">{}</a>".format(
                    item["sent_by_id"],
                    item["sent_by_name"]
                )
            ) + "\n"

    if message.from_user.id in SUDO_USERS:
        await m.edit_text(
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
            ),
            quote=True
        )
    else:
        await m.edit_text(res, disable_web_page_preview=True)


__handlers__ = [
    [
        MessageHandler(
            queue,
            filters.command("queue", "/")
        )
    ]
]
