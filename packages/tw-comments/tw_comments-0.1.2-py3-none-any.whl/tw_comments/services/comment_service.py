import httpx

from datetime import datetime

from ..domains.comment import Comment
from ..domains.author import Author
from ..domains.video import Video


class CommentService:
    __URL = "https://www.googleapis.com/youtube/v3/commentThreads"

    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key

    async def get_comments_by_video(self, video: Video) -> list[Video]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=self.__URL,
                params={
                    "part": "snippet",
                    "videoId": video.id,
                    "maxResults": 50,
                    "key": self.__api_key,
                },
            )
            if response.status_code != 200:
                return []
            return [
                self.__json_item_to_comment(item, video)
                for item in response.json()["items"]
            ]

    def __json_item_to_comment(self, item: dict, video: Video) -> Comment:
        return Comment(
            id=item["id"],
            text=item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
            author=Author(
                name=item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                profile_image_url=item["snippet"]["topLevelComment"]["snippet"][
                    "authorProfileImageUrl"
                ],
            ),
            video=video,
            published_at=datetime.strptime(
                item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                "%Y-%m-%dT%H:%M:%SZ",
            ),
        )
