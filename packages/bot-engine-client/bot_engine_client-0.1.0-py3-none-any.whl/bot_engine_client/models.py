
from typing import Dict
from bot_engine_client.enums import BotType, TradingPlatform


class Bot:
    def __init__(self, id: str, description: str, type: BotType, platform: TradingPlatform) -> None:
        self.__id = id
        self.__description = description
        self.__type = type
        self.__platform = platform

    @property
    def id(self) -> str:
        return self.__id

    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def type(self) -> BotType:
        return self.__type
    
    @property
    def platform(self) -> TradingPlatform:
        return self.__platform
    
    @classmethod
    def from_json(cls, json: Dict) -> "Bot":
        return cls(
            json.get("id", ""),
            json.get("description", ""),
            json.get("type", ""),
            json.get("platform", "")
        )