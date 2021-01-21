import os

if "downloads" not in os.listdir():
    os.mkdir("downloads")

import threading
import queue
import requests
import youtube_dl
import player
from config import DUR_LIMIT, SUDO_USERS
from helpers import format_duration, generate_image

ydl_opts = {"format": "bestaudio/best"}
ydl = youtube_dl.YoutubeDL(ydl_opts)
q = queue.Queue()


def worker():
    while True:
        try:
            item = q.get()

            file_name = ""

            info = ydl.extract_info(item["video"], download=False)

            if (
                int(info["duration"] / 60) > DUR_LIMIT
                and item["play_function"][1][5] not in SUDO_USERS
            ):
                if "on_duration_limit" in item:
                    if item["on_duration_limit"]:
                        args = item["on_duration_limit"][1]
                        args[0] = args[0].format(DUR_LIMIT)
                        item["on_duration_limit"][0](*args)
                q.task_done()
            elif info["is_live"]:
                if "on_is_live_error" in item:
                    if item["on_is_live_error"]:
                        item["on_is_live_error"][0](*item["on_is_live_error"][1])
                q.task_done()
            else:
                file_name = info["id"] + "." + info["ext"]

                args = item["play_function"][1]
                args[0] = "downloads/" + file_name
                args[3] = info["title"]
                args[4] = "https://youtu.be/" + info["id"]
                args[8] = format_duration(info["duration"])

                if file_name not in os.listdir("downloads"):
                    if "on_start" in item:
                        if item["on_start"]:
                            item["on_start"][0](*item["on_start"][1])
                    if args[7]:
                        open("downloads/" + info["id"] + ".png", "wb+").write(
                            requests.get(info["thumbnails"][-1]["url"]).content
                        )
                    ydl.download([item["video"]])
                    os.rename(
                        [i for i in os.listdir() if i.endswith(info["ext"])][0],
                        "downloads/" + file_name,
                    )
                    
                if args[7]:
                    args[7][1][1] = generate_image(
                        "downloads/" + info["id"] + ".png", info["title"], args[6]
                    )

                item["play_function"][0](*args)

                if args[0] == "downloads/" + file_name:
                    if "on_end" in item:
                        if item["on_end"]:
                            item["on_end"][0](*item["on_end"][1])

                q.task_done()
        except:
            if "on_error" in item:
                if item["on_error"]:
                    item["on_error"][0](*item["on_error"][1])
            q.task_done()


threading.Thread(target=worker, daemon=True).start()


def download(
    on_start,
    on_end,
    play_function,
    on_is_live_error,
    video,
    on_error,
    on_duration_limit,
) -> int:
    q.put(
        {
            "on_start": on_start,
            "on_end": on_end,
            "play_function": play_function,
            "on_is_live_error": on_is_live_error,
            "video": video,
            "on_error": on_error,
            "on_duration_limit": on_duration_limit,
        }
    )
    return q.qsize()
