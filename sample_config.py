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

# The ID of the group where your bot streams
GROUP = -1001402753006

# Users must join the group before using the bot (note: the bot should be admin in the group if you enable this)
USERS_MUST_JOIN = False

# Send "now playing" messages to the group
LOG = True

# Choose the preferred language for your bot. If English leave as it is, or change to the code of any supported language.
LANG = "en"

# Max video duration allowed for user downloads in minutes
DUR_LIMIT = 5

# Set to true if song files should be deleted after playing
DELETE_AFTER_PLAYING = True

# No need to touch the following.
LOG_GROUP = GROUP if LOG else None
SUDO_FILTER = filters.user(SUDO_USERS)
