from pyrogram import Client, filters
from pyrogram.types import Message

import player
from helpers import wrap
from config import SUDO_FILTER
from strings import _


@Client.on_message(filters.command("clearqueue", "/") & SUDO_FILTER)
@wrap
def clear_queue(client: Client, message: Message):
    try:
        with player.queue.mutex:
            player.queue.queue.clear()
        message.reply_text(_("queue_4"))
    except:
        message.reply_text(_("error"))


@Client.on_message(filters.command("queue", "/"))
@wrap
def queue(client: Client, message: Message):
    qsize = player.queue.qsize()

    if qsize == 0:
        return

    queue_ = player.queue.queue
    human_queue = _("queue_1").format(qsize) + "\n"
    count = 1

    for item in queue_:
        human_queue += (
            _("queue_2").format(
                count,
                '<a href="{}">{}</a>'.format(
                    item["url"],
                    item["title"],
                ),
                item["duration"],
            )
            + "\n"
        )
        count += 1

    m = message.reply_text("....")

    try:
        m.edit_text(human_queue, disable_web_page_preview=True)
    except:
        m.edit_text(_("error"))


__help__ = {
    "clearqueue": [_("help_clearqueue"), True],
    "queue": [_("help_queue"), False],
}
