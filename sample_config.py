# Just copy this file to config.py and change it to your info.
from pyrogram import filters

# Get these two from https://my.telegram.org
API_ID = 1234567
API_HASH = "ab1c23def45fg67890h123i45678j9kl"

# Get this from @Botfather
TOKEN = "1234567890:ABCdEFgHij1KlMNop_QrStuVWxyzuA-EmXI"

# The IDs of the users which can stream, skip, pause and change volume
SUDO_USERS = [
    383407735,
    951435494,
    1392620345
]


# id of the banned users

BANNED_USERS = [
    1,
    2,
    3
]

# A group ID to send messages to when a song starts playing
# Example group ID: -1001402753006
LOG_GROUP = None  # Just keep it like this if you are not going to use one

# Choose the preferred language for your bot. If English leave as it is, or change to the code of any supported language.
LANG = "en"

# Max video duration allowed for downloads in minutes
DUR_LIMIT = 5

# Show a small credit for @su_Bots in the start message
CREDIT = True

# No need to touch the following.
SUDO_FILTER = filters.user(SUDO_USERS)
BANNED_FILTER = filters.user(BANNED_USERS)
