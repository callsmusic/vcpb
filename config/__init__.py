try:
    from .config import *
except ImportError:
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--api-id",
        help="Telegram api_id, get it from my.telegram.org/apps",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--api-hash",
        help="Telegram api_hash, get it from my.telegram.org/apps",
        required=True,
    )
    parser.add_argument(
        "--bot-token",
        help="Bot token",
        required=True,
    )
    parser.add_argument(
        "--sudo-users",
        help="List of user ids, separate by underscore (example: 1_3)",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--chat-id",
        help="ID of the group where the bot streams",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    API_ID = args.api_id
    API_HASH = args.api_hash
    BOT_TOKEN = args.bot_token
    SUDO_USERS = list(map(int, args.sudo_users.split("_")))
    CHAT_ID = args.chat_id
