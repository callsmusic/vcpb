import pymongo
from config import MONGO_DB_URI


client = pymongo.MongoClient(MONGO_DB_URI)
db = client["vcpb"]
playlist = db["playlist"]


def add_to_playlist(file, title, url, sent_by_id, sent_by_name, duration):
    all_ = playlist.find()

    for item in all_:
        if item["url"] == url:
            return False

    playlist.insert_one(
        {
            "file": file,
            "title": title,
            "url": url,
            "sent_by_id": sent_by_id,
            "sent_by_name": sent_by_name,
            "duration": duration,
        }
    )

    return True


def remove_from_playlist(url):
    all_ = playlist.find()

    for item in all_:
        if item["url"] == url:
            playlist.delete_one({"url": url})
            return True

    return False


def get_playlist():
    all_ = playlist.find()
    all_ = [i for i in all_]

    if len(all_) != 0:
        return all_
    else:
        return False


def remove_all():
    all_ = get_playlist()

    if not all_:
        return False

    for item in all_:
        playlist.delete_one(item["url"])

    return True