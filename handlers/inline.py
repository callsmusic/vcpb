from pyrogram.handlers import InlineQueryHandler
from youtubesearchpython import VideosSearch
from pyrogram.types import (
    CallbackQuery,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from pyrogram import errors


async def search(client, query: CallbackQuery):
    answers = []
    string = query.query.lower()
    if string == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="Start searching youtube videos",
            switch_pm_parameter="help",
            cache_time=0
        )
        return
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description="duration: {}, views: {}".format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Search Timed out! try again",
                switch_pm_parameter="",
            )

__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
