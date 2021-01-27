from pyrogram import filters

try:
    from config.config import *
except ImportError:
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--token",
        help="Bot token",
        required=True,
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
        "--mongodb-uri",
        help="MongoDB URI, if you don't provide the bot will lack some cool features",
        required=False,
        default="",
    )
    parser.add_argument(
        "--sudo-users",
        help="List of user ids, separate by underscore (example: 1_3)",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--group",
        help="Id of the group where the bot streams",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--users-must-join",
        help="If provided, only members of the group can use the bot",
        type=bool,
        required=False,
        default=False,
    )
    parser.add_argument(
        "--lang",
        help="Bot language, choose from strings/",
        required=True,
    )
    parser.add_argument(
        "--dur-limit",
        help="Video download duration limit (in minutes)",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    API_ID = args.api_id
    API_HASH = args.api_hash
    TOKEN = args.token
    MONGO_DB_URI = args.mongodb_uri
    SUDO_USERS = list(map(int, args.sudo_users.split("_")))
    GROUP = args.group
    USERS_MUST_JOIN = args.users_must_join
    LANG = args.lang
    DUR_LIMIT = args.dur_limit
    LOG_GROUP = GROUP if MONGO_DB_URI not in ("", None) else None
    SUDO_FILTER = filters.user(SUDO_USERS)

