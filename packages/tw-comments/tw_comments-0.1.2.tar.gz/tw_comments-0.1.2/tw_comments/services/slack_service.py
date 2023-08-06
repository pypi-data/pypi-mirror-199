import httpx
import json


class SlackService:
    def __init__(self, webhook_url: str) -> None:
        self.__webhook_url = webhook_url

    async def send_message(self, message: dict):
        async with httpx.AsyncClient() as client:
            await client.post(
                url=self.__webhook_url,
                data=json.dumps(message),
                headers={"Content-Type": "application/json"},
            )
