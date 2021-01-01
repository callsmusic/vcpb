from pyrogram import Client
from config import API_ID, API_HASH, TOKEN

app = Client("my_account", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)


if __name__ == "__main__":
    import os
    import sys
    from threading import Thread
    from pyrogram import filters
    import player
    from handlers import all_handlers
    from config import SUDO_FILTER
    from strings import get_string as _

    for handler in all_handlers:
        if len(handler) == 1:
            app.add_handler(handler[0])
        else:
            app.add_handler(handler[0], group=handler[1])

    def stop_and_restart():
        app.stop()
        del player.q
        player.abort()
        os.system("git pull")
        os.execl(sys.executable, sys.executable, *sys.argv)

    @app.on_message(filters.command("r") & SUDO_FILTER)
    async def restart(client, message):
        await message.reply_text(_("bot"))
        Thread(
            target=stop_and_restart
        ).start()

    app.run()
