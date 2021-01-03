import os

if "downloads" not in os.listdir():
    os.mkdir("downloads")

import threading
import queue
import youtube_dl
import player
from config import DUR_LIMIT
from helpers import format_dur

ydl_opts = {
    "format": "bestaudio/best"
}
ydl = youtube_dl.YoutubeDL(ydl_opts)
q = queue.Queue()


def worker():
    while True:
        try:
            item = q.get()

            item["on_start"][0](
                *item["on_start"][1]
            )

            file_name = ""

            info = ydl.extract_info(
                item["video"],
                download=False
            )

            if int(info["duration"] / 60) > DUR_LIMIT:
                args = item["on_dur_limit"][1]
                args[0] = args[0].format(DUR_LIMIT)
                item["on_dur_limit"][0](
                    *args
                )
                q.task_done()
            elif info["is_live"]:
                item["on_is_live_err"][0](
                    *item["on_is_live_err"][1]
                )
                q.task_done()
            else:
                file_name = info["id"] + "." + info["ext"]

                args = item["play_func"][1]
                args[3] = info["title"]
                args[4] = "https://youtu.be/" + info["id"]
                args[8] = format_dur(info["duration"])

                if file_name in os.listdir("downloads"):
                    args[0] = "downloads/" + file_name
                    item["play_func"][0](
                        *args
                    )
                else:
                    ydl.download(
                        [
                            item["video"]
                        ]
                    )
                    os.rename(
                        [
                            i
                            for i in os.listdir()
                            if i.endswith(info["ext"])
                        ][0],
                        "downloads/" + file_name
                    )
                    args[0] = "downloads/" + file_name
                    item["play_func"][0](
                        *args
                    )

                if player.q.qsize() != 0:
                    item["on_end"][0](
                        *item["on_end"][1]
                    )

                q.task_done()
        except:
            item["on_err"][0](
                *item["on_err"][1]
            )
            q.task_done()


threading.Thread(target=worker, daemon=True).start()


def download(on_start, on_end, play_func, on_is_live_err, video, on_err, on_dur_limit):
    q.put(
        {
            "on_start": on_start,
            "on_end": on_end,
            "play_func": play_func,
            "on_is_live_err": on_is_live_err,
            "video": video,
            "on_err": on_err,
            "on_dur_limit": on_dur_limit
        }
    )
    return q.qsize()
