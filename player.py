import os
import threading
import queue
from subprocess import Popen, PIPE
from helpers import run, State

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
                    log = run(item["log"])
            process = Popen(["mplayer", "-novideo", item["stream_url"]], stdin=PIPE)
            process.wait()
        else:
            if "on_start" in item:
                if item["on_start"]:
                    run(item["on_start"], quote=True)

            if "log" in item:
                if item["log"]:
                    caption = item["log"]["kwargs"]["caption"]
                    caption = caption.format(
                        item["url"],
                        item["title"],
                        item["duration"],
                        item["sent_by_id"],
                        item["sent_by_name"],
                    )
                    log = run(item["log"], caption=caption)

            STATE = State.Playing

            process = Popen(["mplayer", "-novideo", item["file"]], stdin=PIPE)
            process.wait()

            if STATE == State.Playing:
                if "on_end" in item:
                    if item["on_end"]:
                        run(item["on_end"], quote=True)
            elif STATE == State.Skipped:
                if "on_skip" in item:
                    if item["on_skip"]:
                        run(item["on_skip"], quote=True)

        process = None
        STATE = State.NothingSpecial

        if log:
            log.delete()

        if q:
            q.task_done()


threading.Thread(target=worker, daemon=True).start()


def play(
    file,
    title,
    duration,
    url,
    sent_by_id,
    sent_by_name,
    log=None,
    on_start=None,
    on_end=None,
    on_skip=None
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
