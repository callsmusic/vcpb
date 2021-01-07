from pyrogram import filters
from pyrogram.handlers import MessageHandler
import player
from helpers import State
from helpers import wrap
from strings import get_string as _


@wrap
def song(client, message):
    m = message.reply_text("....")

    if player.STATE in (State.Playing, State.Paused):
        get = player.q_list[0]
        m.edit_text(
            _("song_1").format(
                "<a href=\"{}\">{}</a>".format(
                    get["url"],
                    get["title"]
                ),
                "<a href=\"tg://user?id={}\">{}</a>".format(
                    get["sent_by_id"],
                    get["sent_by_name"]
                ),
                get["dur"]
            )
        )
    else:
        m.edit_text(
            _("song_2")
        )


__handlers__ = [
    [
        MessageHandler(
            song,
            filters.command("song", "/")
        )
    ]
]
__help__ = {
    "/song": [_("help_song"), False]
}
