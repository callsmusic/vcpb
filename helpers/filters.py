from pyrogram import filters

from config import SUDO_USERS

sudo_only = filters.user(SUDO_USERS)
