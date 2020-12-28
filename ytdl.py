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

        item["on_start"][0](
            *item["on_start"][1],
            quote=True
        )

        file_name = ""

        info = ydl.extract_info(
            item["video"],
            download=False
        )

        if info["is_live"]:
            item["on_is_live_err"][0](
                *item["on_is_live_err"][1],
                quote=True
            )
            q.task_done()
        else:
            file_name = info["id"] + "." + info["ext"]

            if file_name in os.listdir("downloads"):
                args = item["play_func"][1]
                args[0] = "downloads/" + file_name
                args[3] = info["title"]
                args[4] = "https://youtu.be/" + info["id"]
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
                args = item["play_func"][1]
                args[0] = "downloads/" + file_name
                args[3] = info["title"]
                args[4] = "https://youtu.be/" + info["id"]
                item["play_func"][0](
                    *args
                )

            if player.q.qsize() != 0:
                item["on_end"][0](
                    *item["on_end"][1],
                    quote=True
                )

            q.task_done()


threading.Thread(target=worker, daemon=True).start()


def download(on_start, on_end, play_func, on_is_live_err, video):
    q.put(
        {
            "on_start": on_start,
            "on_end": on_end,
            "play_func": play_func,
            "on_is_live_err": on_is_live_err,
            "video": video
        }
    )
    return q.qsize()
