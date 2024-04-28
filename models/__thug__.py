from models import Document


class ThugData(Document):
    """
    ### Attributes
    name `str`
        ex: Thug
    file_name `str`
        ex: thug.png
    exclusive `bool`

    tier `int`

    event `str` | `None`

    release_date `str`
      ex: 13 January 2022
    path `str`
      ex: ./assets/images/thugs/thug.png
    value `int`

    power `int`
    """

    BASE = "thugs"
    name: str
    file_name: str
    exclusive: bool
    tier: int
    event: str = None
    release_date: str
    emoji: str

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.path = f"./assets/images/thugs/{self.file_name}"
        tier, value = 0, 2_517
        while tier != self.tier:
            tier += 1
        value = int(value * 1.37)
        self.value = value
        self.power = 8 * self.tier % 3 + self.tier

    def __str__(self) -> str:
        return self.name

    @classmethod
    def read(cls, id: int):
        data = cls.read_all()
        return data[id]
