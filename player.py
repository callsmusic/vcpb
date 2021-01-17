import os
import threading
import queue
from subprocess import Popen, PIPE
from helpers import State

q = queue.Queue()
currently_playing = {}

process = None
STATE = State.NothingSpecial


def worker():
    global process, STATE, currently_playing
    while True:
        item = q.get()
        currently_playing = item
        log = None

        if "stream_url" in item:
            STATE = State.Streaming
            if "log" in item:
                if item["log"]:
                    log = item["log"][0](*item["log"][1])
            process = Popen(["mplayer", item["stream_url"]], stdin=PIPE)
            process.wait()
        else:
            if "on_start" in item:
                if item["on_start"]:
                    item["on_start"][0](*item["on_start"][1], quote=True)

            if "log" in item:
                if item["log"]:
                    args = item["log"][1]
                    args[2] = args[2].format(
                        item["url"],
                        item["title"],
                        item["duration"],
                        item["sent_by_id"],
                        item["sent_by_name"],
                    )
                    log = item["log"][0](*args)

            STATE = State.Playing

            process = Popen(["mplayer", item["file"]], stdin=PIPE)
            process.wait()

            if STATE == State.Playing:
                if "on_end" in item:
                    if item["on_end"]:
                        item["on_end"][0](*item["on_end"][1], quote=True)
            elif STATE == State.Skipped:
                if "on_skip" in item:
                    if item["on_skip"]:
                        item["on_skip"][0](*item["on_skip"][1], quote=True)

        process = None
        STATE = State.NothingSpecial

        if log:
            log.delete()

        if q:
            q.task_done()


threading.Thread(target=worker, daemon=True).start()


def play(
    file, on_start, on_end, title, url, sent_by_id, sent_by_name, log, duration, on_skip
) -> int:
    q.put(
        {
            "file": file,
            "on_start": on_start,
            "on_end": on_end,
            "title": title,
            "url": url,
            "sent_by_id": sent_by_id,
            "sent_by_name": sent_by_name,
            "log": log,
            "duration": duration,
            "on_skip": on_skip,
        }
    )
    return q.qsize()


def stream(stream_url, log) -> int:
    q.put({"stream_url": stream_url, "log": log})
    return q.qsize()


def is_currently_playing() -> bool:
    return STATE in (State.Playing, State.Paused)


def abort() -> bool:
    if process:
        process.terminate()
        return True
    return False


def pause_resume():
    if process:
        process.stdin.write(b"p")
        process.stdin.flush()
        return True
    return False
