from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import player
from helpers import wrap
from config import SUDO_FILTER
from strings import get_string as _


@Client.on_message(
    filters.command("clearqueue", "/") & SUDO_FILTER
)
@wrap
def clear_queue(client, message):
    try:
        with player.q.mutex:
            player.q.queue.clear()
        message.reply_text(_("queue_4"))
    except:
        message.reply_text(_("error"))


@Client.on_message(
    filters.command("queue", "/")
)
@wrap
def queue(client, message):
    qsize = player.q.qsize()

    if qsize == 0:
        return

    queue_ = player.q.queue
    human_queue = _("queue_1").format(qsize) + "\n"
    count = 1

    for item in queue_:
        human_queue += _("queue_2").format(
            count,
            '<a href="{}">{}</a>'.format(
                item["url"],
                item["title"],
            ),
            item["dur"],
            '<a href="tg://user?id={}">{}</a>'.format(
                item["sent_by_id"],
                item["sent_by_name"],
            ),
        ) + "\n"
        count += 1

    m = message.reply_text("....")
    m.edit_text(human_queue, disable_web_page_preview=True)


__help__ = {
    "clearqueue": [_("help_clearqueue"), True],
    "queue": [_("help_queue"), False]
}
