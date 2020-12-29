from pyrogram import Client
from config import API_ID, API_HASH, TOKEN

app = Client("my_account", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)


if __name__ == "__main__":
    from handlers import all_handlers

    for handler in all_handlers:
        if len(handler) == 1:
            app.add_handler(handler[0])
        else:
            app.add_handler(handler[0], group=handler[1])

    app.run()
