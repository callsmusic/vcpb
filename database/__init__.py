import sys
from pymongo import MongoClient

from config import MONGO_DB_URI


try:
    URI = MONGO_DB_URI
    client = MongoClient(URI)
    db = client["vcpb"]
except:
    print("Invalid MongoDB URI was provided.")
    sys.exit()

"""

Structure:

[database]VCPB
├───[table]playlists
│   ├───[column]name: str
│   └───[column]items: list(dict(url: str, title: str))
├───[table]sudo_users
│   ├───[column]id: int
│   ├───[column]first: str
│   ├───[column]last: str | NoneType
│   └───[column]username: str | NoneType
└───[table]banned_users
    ├───[column]id: int
    ├───[column]first: str
    ├───[column]last: str | NoneType
    └───[column]username: str | NoneType

Playlists example:

(
    name="custom",
    items=[
        {
            "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk&feature=youtu.be",
            title: "Luis Fonsi - Despacito ft. Daddy Yankee",
        },
        ...
    ]
)

Sudo/banned users example:

(
    id=42777,
    first="Telegram",
    last=None,
    username=None
)

"""
