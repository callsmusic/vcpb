from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import player
from helpers import wrap
from strings import _


@Client.on_message(filters.command("song", "/"))
@wrap
def mistake(client, message):
    if player.is_currently_playing():
        message.reply_text(
            _("song_1").format(
                '<a href="{}">{}</a>'.format(
                    player.currently_playing["url"], player.currently_playing["title"]
                ),
                player.currently_playing["duration"],
                '<a href="tg://user?id{}">{}</a>'.format(
                    player.currently_playing["sent_by_id"],
                    player.currently_playing["sent_by_name"],
                ),
            )
        )
    else:
        message.reply_text(_("song_2"))
