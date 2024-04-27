from models.__schema__ import Directory
from models.__thug__ import ThugData
import json

class CardData(Directory):
    BASE = "card"
    KEYS = ["level", "amount", "power"]
    id: int
    level: int
    amount: int
    power: int
    thug: ThugData

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.thug = ThugData.read(self.id)

        def get_level(level):
            if level > 24:
                return ""
            if level in [0, 3, 8, 14, 24]:
                return str(level)
            return get_level(level + 1)

        with open("./data/extras.json", "r") as file:
            extras = json.load(file)
            
        self.extra = extras.get()
