import threading
import queue
from subprocess import Popen, PIPE

q = queue.Queue()
q_list = []

process = None


def worker():
    global current, process, q_list
    while True:
        item = q.get()
        log = None

        if "stream_url" in item:
            if "log" in item:
                if item["log"]:
                    log = item["log"][0](
                        *item["log"][1]
                    )
            process = Popen(["mplayer", item["stream_url"]], stdin=PIPE)
            process.wait()
        else:
            item["start"][0](
                *item["start"][1],
                quote=True
            )

            if "log" in item:
                if item["log"]:
                    args = item["log"][1]
                    args[1] = args[1].format(
                        item["url"],
                        item["title"],
                        item["sent_by_id"],
                        item["sent_by_name"],
                        item["dur"]
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
            del q_list[0]
        if log:
            log.delete()

        process = None
        q.task_done()


threading.Thread(target=worker, daemon=True).start()


def play(file, start, end, title, url, sent_by_id, sent_by_name, log, dur):
    args = {
        "file": file,
        "start": start,
        "end": end,
        "title": title,
        "url": url,
        "sent_by_id": sent_by_id,
        "sent_by_name": sent_by_name,
        "log": log,
        "dur": dur
    }
    q.put(
        args
    )
    q_list.append(
        args
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
    return q_list[0] if q_list else False


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
