import os

if not os.path.isdir(os.path.realpath("../downloads")):
    os.mkdir(os.path.realpath("../downloads"))

import threading
import queue
import youtube_dl
from helpers.queues import run
from helpers.duration import format_duration

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
    'quiet': True,
}
ydl = youtube_dl.YoutubeDL(ydl_opts)
queue = queue.Queue()


def worker():
    while True:
        item = queue.get()

        try:
            info = ydl.extract_info(item["video"], download=False)

            if info["is_live"]:
                run(item["on_is_live_error"])
                queue.task_done()
            else:
                file_name = f"{info['id']}.{info['ext']}"
                if file_name not in os.listdir("../downloads"):
                    run(item["on_start"])
                    ydl.download([item["video"]])
                run(
                    item["play_function"],
                    file="downloads/" + file_name,
                    title=info["title"],
                    duration=format_duration(info["duration"]),
                    url=f"https://youtu.be/{info['id']}",
                )
                run(item["on_end"])
                queue.task_done()
        except Exception as e:
            item["on_error"]["args"][0] = item["on_error"]["args"][0].format(type(e).__name__, e)
            run(item["on_error"])
            queue.task_done()


threading.Thread(target=worker, daemon=True).start()


def download(*_, **kwargs) -> int:
    queue.put({**kwargs})
    return queue.qsize()
