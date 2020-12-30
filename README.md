# Pyrogram bot to automate streaming music in voice chats

## Help
If you face an error, want to discuss this project or get support for it join [@su_Chats](https://t.me/su_Chats).

## Inspiration
Enormous and huge credits to [@itayki](https://t.me/itayki) from Israel for being with me while
waiting for Mr. [@TwitFace, AKA Andrew Lungers](https://t.me/TwitFace) to release [pytgcalls](https://github.com/pytgcalls/pytgcalls) to write this bot.

## Idea
From Mr. [@TwitFace, AKA Andrew Lungers](https://t.me/TwitFace).

## Requirements
* A computer running a Linux distribution with a desktop environment (if you are on VPS and don't have one, refer to [this](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/use-remote-desktop)),
* the latest version of Telegram desktop,
* `pulseaudio` (installation on Ubuntu: `apt install pulseaudio`),
* `mplayer` (installation on Ubuntu: `apt install mplayer`),
* `python3` (installation on Ubuntu: `apt install python3`) and
* `python3-pip` (installation on Ubuntu: `apt install python3-pip`) installed on it.

## Running
1. Make sure you are not running any command as root, to avoid bulky errors.
2. Clone the repository and change the dir:
```
    git clone https://github.com/suprojects/VoiceChatPyroBot.git tgvcbot && cd tgvcbot
```
3. Copy `sample_config.py` to `config.py` and make it use your credentials:

    `API_ID` int: your api id from [my.telegram.org](https://my.telegram.org)

    `API_HASH` str: your api hash from [my.telegram.org](https://my.telegram.org)

    `TOKEN` str: your bot token from [@BotFather](https://t.me/BotFather)

    `SUDO_USERS` list(int): a list of user ids which can pause, skip and change volume

    `LOG_GROUP` int: (optional) a group chat id to send "now playing" messages to in a non-spammy way
    
    `LANG` str: your bot language, choose an available language code in [strings/](https://github.com/suprojects/VoiceChatPyroBot/tree/main/strings)
    
    `DUR_LIMIT` int: max video duration in minutes for downloads

4. Install the required Python packages:
```
    pip(3) install -U -r requirements.txt
```
5. Make sure pulseaudio is running and load a null sink named `MySink` by running:
```
    bash pa.sh
```
6. Run the bot:
```
    python(3) bot.py
```
7. Open Telegram desktop, join a voice chat and set `MySink.monitor` as your microphone, if you can't see `MySink.monitor`:
    1. Open pulseaudio volume control (pavuvontrol).
    2. The configurations tab.
    3. Turn the configs/profiles you see off.
9. Once you've done the steps above, you can start using and sending commands to your bot to stream in the voice chat you are currently in with Telegram desktop!

