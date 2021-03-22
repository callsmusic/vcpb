import threading
from queue import Queue
from mpv import MPV
from helpers.queues import run

mpv = MPV()
queue = Queue()
streaming = []


def worker():
    while True:
        item = queue.get()
        run(item["on_start"], quote=True)
        item["log"]["args"][1] = item["log"]["args"][1].format(
            item["url"],
            item["title"],
            item["duration"],
        )
        log = run(item["log"])
        mpv.play(item["file"])
        mpv.wait_for_playback()
        run(item["on_end"], quote=True)
        log.delete()
        queue.task_done()


threading.Thread(target=worker, daemon=True).start()


def play(*_, **kwargs):
    queue.put({**kwargs})


def is_streaming():
    return bool(streaming)


def stream(url: str):
    streaming.append(0)
    mpv.play(url)


def stop_streaming() -> bool:
    if is_streaming():
        del streaming[0]
        mpv.stop()
        return True
    else:
        return False
