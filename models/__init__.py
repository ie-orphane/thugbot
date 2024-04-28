from models.__schema__ import Model, ModelEncoder, Document, Collection, Directory
from models.__thug__ import ThugData
from models.__card__ import CardData
from models.__hunter__ import HunterData


class Emoji:
    coin = "<:thugCoin:1089857136726646805>"
    star = "<:thugStar:1089857140832870430>"
    xp = "<:thugXP:1089857138383401122>"
    level = "<:lvl1:1093867735408197732>"
    highLevel = "<:lvl5:1093867749547196527>"
    empty = "<:empty:1144234051947999322>"

    # chest = "<:chest:1147865317876432926>"
    # card = "<:card:1089855288259137576>"

    # trophy = "<:trophy:1089855257007366214>"
    # member = "<:members:1106897019898961950>"
    # rank = "<:rank:1092956484729573450>"
    # game = "<:game:1089853943682699325>"


class Dot:
    orange = "<:orangeDot:1089853960338288681>"
    blue = "<:blueDot:1089853939496800317>"
    black = "<:blackDot:1089853937550622773>"
    purple = "<:purpleDot:1089853970161344553>"
    green = "<:greenDot:1089853934799175720>"
    red = "<:redDot:1089853933029163028>"
    pink = "<:pinkDot:1089853968450072646>"
    yellow = "<:yellowDot:1089853977262297219>"

    def rarity(rarity: str):
        return {
            "unreal": "<:greenDot:1089853934799175720>",
            "common": "<:blueDot:1089853939496800317>",
            "rare": "<:orangeDot:1089853960338288681>",
            "epic": "<:purpleDot:1089853970161344553>",
            "legendary": "<:redDot:1089853933029163028>",
            "exclusive": "<:pinkDot:1089853968450072646>",
            "thugraculous": "<:yellowDot:1089853977262297219>",
        }.get(rarity)
