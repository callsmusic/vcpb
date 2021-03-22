import os

from pyrogram import Client, filters
from pyrogram.types import Message

from helpers.filters import sudo_only
from helpers.decorators import errors

downloads = os.path.realpath("downloads")


@Client.on_message(
    filters.command(["rmd", "rm_downloads", "rmdownloads", "clear_downloads", "cleardownloads"])
    & sudo_only
)
@errors
def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads)
    if ls_dir:
        for file in os.listdir(downloads):
            os.remove(os.path.join(downloads, file))
        message.reply_text("<b>✅ Deleted all downloaded files</b>", quote=False)
    else:
        message.reply_text("<b>❌ Nothing is downloaded to delete</b>", quote=False)
