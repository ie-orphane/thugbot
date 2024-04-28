from typing import Literal
from models import Directory, ThugData


class CardData(Directory):
    BASE = "card"
    KEYS = ["level", "amount", "power"]
    id: int
    level: int
    amount: int
    power: int
    thug: ThugData
    rarity: Literal["unreal", "common", "rare", "epic", "legendary", "thugraculous"]
    color: int
    factor: int
    cards: int
    points: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.thug = ThugData.read(self.id)

        def get_level(level):
            if level > 24:
                return ""
            if level in [0, 3, 8, 14, 24]:
                return str(level)
            return get_level(level + 1)

        self.__dict__.update(
            {
                "0": {
                    "rarity": "unreal",
                    "color": 1752220,
                    "factor": 90,
                    "cards": 21,
                    "points": 1,
                },
                "3": {
                    "rarity": "common",
                    "color": 3447003,
                    "factor": 66,
                    "cards": 17,
                    "points": 4,
                },
                "8": {
                    "rarity": "rare",
                    "color": 15105570,
                    "factor": 23,
                    "cards": 13,
                    "points": 7,
                },
                "14": {
                    "rarity": "epic",
                    "color": 10181046,
                    "factor": 14,
                    "cards": 10,
                    "points": 11,
                },
                "24": {
                    "rarity": "legendary",
                    "color": 15418782,
                    "factor": 6,
                    "cards": 8,
                    "points": 15,
                },
                "": {
                    "rarity": "thugraculous",
                    "color": 15844367,
                    "factor": 1,
                    "cards": 3,
                    "points": 26,
                },
            }.get(get_level(self.level))
        )
