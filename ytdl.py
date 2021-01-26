import os

if "downloads" not in os.listdir():
    os.mkdir("downloads")

import threading
import queue
import requests
import youtube_dl
from config import DUR_LIMIT, SUDO_USERS
from helpers import run, format_duration, generate_image

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = youtube_dl.YoutubeDL(ydl_opts)
q = queue.Queue()


def worker():
    while True:
        item = q.get()

        try:
            info = ydl.extract_info(item["video"], download=False)

            if (
                int(info["duration"] / 60) > DUR_LIMIT
                and item["play_function"]["kwargs"]["sent_by_id"] not in SUDO_USERS
            ):
                if "on_duration_limit" in item:
                    if item["on_duration_limit"]:
                        item["on_duration_limit"]["args"][0] = item["on_duration_limit"]["args"][0].format(DUR_LIMIT)
                        run(item["on_duration_limit"])
                q.task_done()
            elif info["is_live"]:
                if "on_is_live_error" in item:
                    if item["on_is_live_error"]:
                        run(item["on_is_live_error"])
                q.task_done()
            else:
                file_name = info["id"] + "." + info["ext"]
                _log = item["play_function"]["kwargs"]["log"]

                if file_name not in os.listdir("downloads"):
                    if "on_start" in item:
                        if item["on_start"]:
                            run(item["on_start"])
                    if _log:
                        open("downloads/" + info["id"] + ".png", "wb+").write(
                            requests.get(info["thumbnails"][-1]["url"]).content
                        )
                    ydl.download([item["video"]])

                if _log:
                    _log["kwargs"]["photo"] = generate_image(
                        "downloads/" + info["id"] + ".png",
                        info["title"],
                        item["play_function"]["kwargs"]["sent_by_name"]
                    )

                run(
                    item["play_function"],
                    file="downloads/" + file_name,
                    title=info["title"],
                    duration=format_duration(info["duration"]),
                    url="https://youtu.be/" + info["id"],
                    log=_log,
                )

                if "on_end" in item:
                    if item["on_end"]:
                        run(item["on_end"])

                q.task_done()
        except:
            if "on_error" in item:
                if item["on_error"]:
                    run(item["on_error"])
            q.task_done()


threading.Thread(target=worker, daemon=True).start()


def download(
    video,
    play_function,
    on_start=None,
    on_end=None,
    on_is_live_error=None,
    on_error=None,
    on_duration_limit=None,
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
