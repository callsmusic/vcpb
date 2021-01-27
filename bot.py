from pyrogram import Client
from config import API_ID, API_HASH, TOKEN, LOG_GROUP


app = Client(
    "my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins={"root": "handlers", "exclude": None if LOG_GROUP else ["playlist"]}
)


if __name__ == "__main__":
    import os
    import sys
    from threading import Thread
    from pyrogram import idle, filters
    from pyrogram.handlers import MessageHandler
    import player
    from config import SUDO_FILTER
    from strings import _

    def stop_and_restart():
        app.stop()
        player.q = None
        player.abort()
        os.system("git pull")
        os.execl(sys.executable, sys.executable, *sys.argv)

    @app.on_message(filters.command("r", "/") & SUDO_FILTER)
    def restart(client, message):
        message.reply_text(_("bot"))
        Thread(
            target=stop_and_restart
        ).start()

    app.start()
    idle()
