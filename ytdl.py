import os

if "downloads" not in os.listdir():
    os.mkdir("downloads")

import threading
import queue
import youtube_dl
import player

ydl_opts = {
    "format": "bestaudio/best"
}
ydl = youtube_dl.YoutubeDL(ydl_opts)
q = queue.Queue()


def worker():
    while True:
        item = q.get()
        start_func = item["start"]
        start_func[0](*start_func[1], quote=True)
        end_func = item["end"]
        play_func = item["play"]
        vid = item["vid"]

        file_name = ""

        info = ydl.extract_info(
            vid,
            download=False
        )

        file_name = info["id"] + "." + info["ext"]

        if file_name in os.listdir("downloads"):
            args = play_func[1]
            args[0] = "downloads/" + file_name
            args[3] = info["title"]
            args[4] = "https://youtu.be/" + info["id"]
            play_func[0](*args)
        else:
            ydl.download([vid])
            os.rename(
                [
                    i
                    for i in os.listdir()
                    if i.endswith(info["ext"])
                ][0],
                "downloads/" + file_name
            )
            args = play_func[1]
            args[0] = "downloads/" + file_name
            args[3] = info["title"]
            args[4] = "https://youtu.be/" + info["id"]
            play_func[0](*args)

        if player.q.qsize() != 0:
            end_func[0](*end_func[1], quote=True)

        q.task_done()


threading.Thread(target=worker, daemon=True).start()


def download(start, end, play, vid):
    q.put(
        {
            "start": start,
            "end": end,
            "play": play,
            "vid": vid
        }
    )
    return q.qsize()
