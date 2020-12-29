# Pyrogram bot to automate streaming music in voice chats

## Help
If you face an error, want to discuss this project or get support for it join [@su_Chats](https://t.me/su_Chats).

## Inspiration
Enormous and huge credits to [@itayki](https://t.me/itayki) from Israel for being with me while
waiting for Mr. [@TwitFace, AKA Andrew Lungers](https://t.me/TwitFace) to release [pytgcalls](https://github.com/pytgcalls/pytgcalls) to write this bot.

## Idea
From Mr. [@TwitFace, AKA Andrew Lungers](https://t.me/TwitFace).

## Requirements
* A computer running a Linux distribution with a desktop environment,
* the latest version of Telegram desktop,
* `pulseaudio` (installation on Ubuntu: `apt install pulseaudio`),
* `mplayer` (installation on Ubuntu: `apt install mplayer`),
* `python3` (installation on Ubuntu: `apt install python3`) and
* `python3-pip` (installation on Ubuntu: `apt install python3-pip`) installed on it.

## Running
1. Clone the repository and change the dir:
```
    git clone https://github.com/suprojects/VoiceChatPyroBot.git tgvcbot && cd tgvcbot
```
2. Modify `sample_config.py` to use your credenitals and then rename/copy it to `config.py`:

    `API_ID`: your api id from [my.telegram.org](https://my.telegram.org)

    `API_HASH`: your api hash from [my.telegram.org](https://my.telegram.org)

    `TOKEN`: your bot token from [@BotFather](https://t.me/BotFather)

    `SUDO_USERS`: a list of user ids which can pause, skip and change volume

    `LOG_GROUP`: (optional) a group chat id to send "now playing" messages to in a non-spammy way

3. Install the required Python packages:
```
    pip(3) install -U -r requirements.txt
```
4. Make sure pulseaudio is running and load a null sink named `MySink` by running:
```
    bash pa.sh
```
5. Run the bot:
```
    python(3) bot.py
```
6. Open Telegram desktop, join a voice chat and set `MySink` as your microphone.
7. Once you've done the steps above, you can start using and sending commands to your bot to stream in the voice chat you are currently in with Telegram desktop!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/profiregod/VoiceChatPyroBot.git)
