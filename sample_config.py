# Just change the info below and rename this file to config.py

from pyrogram import filters

API_ID = 1234567
API_HASH = "ab1c23def45fg67890h123i45678j9kl"
TOKEN = "1234567890:ABCdEFgHij1KlMNop_QrStuVWxyzuA-EmXI"
SUDO_USERS = [
    383407735,
    951435494,
    1392620345
]
LOG_GROUP = None # Just keep it like this if you are not going to use one

# No need to touch this
SUDO_FILTER = filters.user(SUDO_USERS)
