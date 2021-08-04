# 🎧 VoiceChatPyroBot — The first Telegram voice chat bot to be open-sourced [![Mentioned in Awesome Telegram Calls](https://awesome.re/mentioned-badge-flat.svg)](https://github.com/tgcalls/awesome-tgcalls)

## 💭 Logic

The only thing VCPB does for you is automating the audio streaming process, it doesn’t directly play audio in group calls. So you have to forward the audio that VCPB plays to a Telegram call manually using Telegram desktop app on your PC or server with a desktop environment.

### 🛠 Config

Pass CLI args when running or copy config/sample_config.py to config/config.py
    
### ✍️ Install the required packages

```shell
sudo apt install mpv libmpv-dev pulseaudio &&
pip3 install -U -r requirements.txt
```
### ✨ Run the bot

```shell
python3 main.py  
```

## ℹ️ Commands

### 👥 Everyone

- Sending a YouTube video link in private downloads and adds it to the queue if no radio is streaming.

| Command | Description                                 |
| ------- | ------------------------------------------- |
| /queue  | see the items in the queue if there are any |


### 👤 Sudo users

| Command | Description                                                   |
| ------- | ------------------------------------------------------------- |
| /stream | stream the provided radio station if not streaming            |
| /stop   | stop the radio stream if streaming                            |
| /pause  | pause the audio stream if not playing                         |
| /resume | resume the audio stream if not paused                         |
| /skip   | skip the current audio stream if playing                      |
| /clear  | clear the queue if not empty                                  |
| /rmd    | delete the downloaded files if there are any                  |
| /seekf  | seek the playback forward by the provided seconds if playing  |
| /seekb  | seek the playback backward by the provided seconds if playing |

## 📄 License

### GNU Affero General Public License v3.0

[Read more](http://www.gnu.org/licenses/#AGPL)
