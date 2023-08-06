class Author:
    def __init__(self, name: str, profile_image_url: str) -> None:
        self.__name = name
        self.__profile_image_url = profile_image_url

    @property
    def name(self) -> str:
        return self.__name

    @property
    def profile_image_url(self) -> str:
        return self.__profile_image_url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return NotImplemented
        return (
            self.name == other.name
            and self.profile_image_url == other.profile_image_url
        )

    def __repr__(self) -> str:
        return f"Author(name={self.name}, profile_image_url={self.profile_image_url})"

    def __str__(self) -> str:
        return f"Author(name={self.name}, profile_image_url={self.profile_image_url})"

    def __hash__(self) -> int:
        return hash((self.name, self.profile_image_url))
