class Video:
    def __init__(self, id: str, title: str, link: str) -> None:
        self.__id = id
        self.__title = title
        self.__link = link

    @property
    def id(self) -> str:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def link(self) -> str:
        return self.__link

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Video):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        return f"Video(id={self.id}, title={self.title}, link={self.link})"

    def __str__(self) -> str:
        return f"Video(id={self.id}, title={self.title}, link={self.link})"

    def __hash__(self) -> int:
        return hash((self.id, self.title, self.link))
