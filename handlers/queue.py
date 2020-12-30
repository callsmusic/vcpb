from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from config import SUDO_FILTER
from strings import get_string as _


async def queue(client, message):
    first_10 = player.q_list[:10]
    res = (_("listing") + "\n\n").format(
        len(first_10),
        len(player.q_list)
    )

    if first_10:
        for i in range(len(first_10)):
            item = first_10[i]
            res += _("list_item").format(
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

    await message.reply_text(res, disable_web_page_preview=True)


__handlers__ = [
    [
        MessageHandler(
            queue,
            filters.command("queue", "/")
        )
    ]
]
