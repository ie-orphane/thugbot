import os
import json
import random
from typing import Literal
from models import Collection, CardData, ThugData
from datetime import datetime, UTC, timedelta


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
        if data_dict["created_at"] != None:
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

    def check_cooldown(self, label: Literal["claim"]):
        if self.cooldowns[label] != None:
            available_time = datetime.fromisoformat(self.cooldowns[label]) + timedelta(
                seconds={
                    "claim": 3_600,
                    "streetfight": 3_600,
                    "hangthug": 5_400,
                    "pvb": 5_400,
                    "tictugtoe": 5_400,
                    "guesscountry": 5_400,
                    "sudoku": 5_400,
                    "thuggame": 1_800,
                    "shop": 43_200,
                    "Topgg": 43_200,
                    "DiscordBotList": 43_200,
                    "collect": 86_400,
                }[label]
            )
            if not available_time < datetime.now(UTC):
                cooldown_time = str(available_time - datetime.now(UTC)).split(".")[0]
                self.update()
                return True, f"**{cooldown_time}** <a:clock:1089855473672536064>"

        self.cooldowns[label] = str(datetime.now(UTC))
        return False, None

    def claim_thug(self) -> CardData:
        claim_list = []
        for index, thug in enumerate(ThugData.read_all()):
            thug_card = CardData.read(_id=self.id, id=index)
            fac = 100 if thug_card is None else thug_card.factor
            for _ in range(fac):
                claim_list.append((index, thug, thug_card))
        random.shuffle(claim_list)
        thug_id, thug, card = random.choice(claim_list)

        if card is None:
            card = CardData(
                _id=self.id, id=thug_id, level=0, amount=0, power=thug.power
            )
            self.star += 3
        else:
            card.amount += 1
            self.star += 1
        self.update()
        return card.update()

    @property
    def gang(self):
        class Gang:
            total = 0
            collected = 0
            x = 0
            all: dict[str, list[CardData]] = {}
            value = 0

        for card in CardData.read_all(self.id):
            amount = card.amount + card.level * card.cards
            Gang.total += amount
            if card.thug.exclusive:
                Gang.x += 1
            else:
                Gang.collected += 1
            Gang.value += card.thug.value * amount
            Gang.all.setdefault(card.rarity, [])
            Gang.all[card.rarity].append(card)

        return Gang
