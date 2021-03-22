from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "handlers"}
)

if __name__ == "__main__":
    bot.run()
