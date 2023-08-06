from datetime import datetime

from .author import Author
from .video import Video


class Comment:
    def __init__(
        self, id: str, text: str, author: Author, video: Video, published_at: datetime
    ) -> None:
        self.__id = id
        self.__text = text
        self.__author = author
        self.__video = video
        self.__published_at = published_at

    @property
    def id(self) -> str:
        return self.__id

    @property
    def text(self) -> str:
        return self.__text

    @property
    def author(self) -> Author:
        return self.__author

    @property
    def published_at(self) -> datetime:
        return self.__published_at

    @property
    def video(self) -> Video:
        return self.__video

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Comment):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        return f"Comment(id={self.id}, text={self.text}, author={self.author}, video={self.video}, published_at={self.published_at})"

    def __str__(self) -> str:
        return f"Comment(id={self.id}, text={self.text}, author={self.author}, video={self.video}, published_at={self.published_at})"

    def __hash__(self) -> int:
        return hash((self.id, self.text, self.author, self.published_at))
