import json
import os
from models.__schema__ import Collection
from datetime import datetime, UTC


class HunterData(Collection):
    BASE = "hunter"
    id: int
    coin: int
    xp: int
    star: int
    level: int
    streak: dict[str, int]
    created_at: datetime

    def __to_dict__(self):
        data_dict = super().__to_dict__()
        data_dict["created_at"] = str(data_dict["created_at"])
        return data_dict

    @classmethod
    def create(cls, id: int | str):
        data = cls(
            id=id,
            coin=0,
            xp=0,
            star=0,
            level=0,
            streak={"interaction": 0, "Topgg": 0, "DiscordBotList": 0},
            created_at=datetime.now(UTC),
        )
        os.mkdir(f"./data/card/{id}")
        return data.update()

    @classmethod
    def read(cls, id: int | str):
        try:
            with open(f"./data/{cls.BASE}/{id}.json", "r") as file:
                data: dict = json.load(file)
        except FileNotFoundError:
            return None
        else:
            if data["created_at"] != None:
                data["created_at"] = datetime.fromisoformat(data["created_at"])
            return cls(id=int(id), **data)

    def interaction(self, command: str):
        with open("./data/interactions.csv", "a") as file:
            file.write(f"\n{datetime.now(UTC)},{self.id},{command}")
        self.streak["interaction"] += 1
        self.update()

    def required_xp(self):
        """calculate the required amount of xp"""
        old = 0 if self.level == 0 else int((2 * (self.level - 1) + 1) * 10**2 * 0.69)
        reXP = (2 * self.level + 1) * 10**2 + old
        return reXP
