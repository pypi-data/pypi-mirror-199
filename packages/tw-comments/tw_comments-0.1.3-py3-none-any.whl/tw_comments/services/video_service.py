import httpx

from ..domains.video import Video


class VideoService:
    __URL = "https://www.googleapis.com/youtube/v3/playlistItems"

    def __init__(self, api_key: str):
        self.__api_key = api_key

    def __get_videos_page_by_playlist(
        self,
        playlist_id: str,
        max_results=50,
        part="snippet,contentDetails",
        page_token: str = None,
    ):
        params = {
            "part": part,
            "playlistId": playlist_id,
            "maxResults": max_results,
            "key": self.__api_key,
        }
        if page_token is not None:
            params["pageToken"] = page_token
        response = httpx.get(self.__URL, params=params)
        response.raise_for_status()
        return response.json()

    def get_videos_page_by_playlist(
        self,
        playlist_id: str,
        max_results=50,
        part="snippet,contentDetails",
        page_token: str = None,
    ) -> list[Video]:
        response = self.__get_videos_page_by_playlist(
            playlist_id=playlist_id,
            max_results=max_results,
            part=part,
            page_token=page_token,
        )
        return [self.__json_item_to_video(item) for item in response["items"]]

    def get_all_videos_by_playlist(
        self,
        playlist_id: str,
        part="snippet,contentDetails",
    ) -> list[Video]:
        videos: list[Video] = []
        next_page_token = None
        while True:
            response = self.__get_videos_page_by_playlist(
                playlist_id=playlist_id,
                part=part,
                page_token=next_page_token,
            )
            videos.extend(
                [self.__json_item_to_video(item) for item in response["items"]]
            )
            if "nextPageToken" in response:
                next_page_token = response["nextPageToken"]
            else:
                break
        return videos

    def __json_item_to_video(self, item: dict) -> Video:
        return Video(
            id=item["contentDetails"]["videoId"],
            title=item["snippet"]["title"],
            link=f"https://www.youtube.com/watch?v={item['contentDetails']['videoId']}",
        )
