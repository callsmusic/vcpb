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


__help__ = {
    "clearqueue": [_("help_clearqueue"), True]
}
