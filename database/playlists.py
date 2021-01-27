from database import db


playlists = db["playlists"]


def create_playlist(name: str) -> bool:
    playlist = playlists.find_one({"name": name})

    if playlist:
        return False
    else:
        playlists.insert_one(
            {"name": name, "items": []}
        )
        return True


def get_playlist(name: str):
    playlist = playlists.find_one({"name": name})

    if not playlist:
        return False
    else:
        return playlist


def add_item_to_playlist(name: str, item: dict) -> bool:
    playlist = get_playlist(name)

    if not playlist:
        return False
    else:
        items = playlist["items"]
        urls = [i["url"] for i in items]

        if item["url"] in urls:
            return False

        items.append(item)

        playlists.update_one(
            {"name": name},
            {
                "$set": {"items": items}
            }
        )
        return True


def remove_item_from_playlist(name: str, item: dict) -> bool:
    playlist = get_playlist(name)

    if not playlist:
        return False
    else:
        items = playlist["items"]
        urls = [i["url"] for i in items]

        if item["url"] not in urls:
            return False

        items.remove(item)

        playlists.update_one(
            {"name": name},
            {
                "$set": {"items": items}
            }
        )
        return True


def reset_playlist(name: str, items: list) -> bool:
    playlist = get_playlist(name)

    if not playlist:
        return False
    else:
        if playlist["items"] == items:
            return False

        playlists.update_one(
            {"name": name},
            {
                "$set": {"items": items}
            }
        )
        return True


def delete_playlist(name: str) -> bool:
    playlist = get_playlist(name)

    if not playlist:
        return False
    else:
        playlists.delete_one(
            {"name": name}
        )