import threading
import queue
from subprocess import Popen, PIPE

q = queue.Queue()

process = None
current = {}


def worker():
    global current, process
    while True:
        item = q.get()
        log = None

        if "stream_url" in item:
            if "log" in item:
                log = item["log"][0](
                    item["log"][1]
                )
            process = Popen(["mplayer", item["stream_url"]], stdin=PIPE)
            process.wait()
        else:
            current = item
            item["start"][0](
                *item["start"][1],
                quote=True
            )

            if "log" in item:
                args = item["log"][1]
                args[1] = args[1].format(
                    item["url"],
                    item["title"],
                    item["sent_by_id"],
                    item["sent_by_name"]
                )
                log = item["log"][0](
                    *args
                )
            process = Popen(["mplayer", item["file"]], stdin=PIPE)
            process.wait()
            item["end"][0](
                *item["end"][1],
                quote=True
            )
            current = {}

        if log:
            log.delete()

        process = None
        q.task_done()


threading.Thread(target=worker, daemon=True).start()


def play(file, start, end, title, url, sent_by_id, sent_by_name, log):
    q.put(
        {
            "file": file,
            "start": start,
            "end": end,
            "title": title,
            "url": url,
            "sent_by_id": sent_by_id,
            "sent_by_name": sent_by_name,
            "log": log
        }
    )
    return q.qsize()


def stream(stream_url, log):
    q.put(
        {
            "stream_url": stream_url,
            "log": log
        }
    )
    return q.qsize()


def currently_playing():
    return current


def abort():
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
