from pyrogram import Client, filters
from pyrogram.types import Message

import player
from helpers import wrap
from strings import _


@Client.on_message(filters.command("song", "/"))
@wrap
def mistake(client: Client, message: Message):
    if player.is_currently_playing():
        message.reply_text(
            _("song_1").format(
                '<a href="{}">{}</a>'.format(
                    player.currently_playing["url"], player.currently_playing["title"]
                ),
                player.currently_playing["duration"],
            )
        )
    else:
        message.reply_text(_("song_2"))
