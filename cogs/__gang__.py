import discord
from discord.ext import commands
from models import Emoji, Dot, ThugData
from typing import Optional
from models import HunterData
from cogs import Cog
from tabulate import tabulate


def HunterEmbed(
    member: discord.Member | discord.User,
    highLevel: bool = True,
    level: str | int = "***\u221E***",
    xp: str = "***\u221E***",
    coins: str = "***\u221E***",
    stars: str = "***\u221E***",
):
    return discord.Embed(
        color=discord.Color.dark_blue(),
        description=(
            f"{Emoji.highLevel if highLevel else Emoji.level} Level\u1CBC:\u1CBC{level}\n"
            f"{Emoji.xp} XP{'\u1CBC'*3}:\u1CBC{xp}"
            f"\n{Emoji.star} Stars\u1CBC:\u1CBC{stars}"
            f"\n{Emoji.coin} Coins\u1CBC:\u1CBC{coins}"
        ),
    ).set_author(name=f"{member}", icon_url=member.avatar)


class Gang(Cog):
    @discord.app_commands.command(description="Show your gang")
    async def gang(
        self, interaction: discord.Interaction, member: Optional[discord.Member] = None
    ):
        try:
            await interaction.response.defer()
            self.interaction = interaction
            self.start()
            member = member or interaction.user

            if member.id == 1063459223289200652:
                thugs, elite, exclusive = (
                    f"\n\n**{Dot.green} Thugs**",
                    f"\n\n**{Dot.yellow} Elite Thugs**",
                    f"\n\n**{Dot.pink} Exclusive Thugs**",
                )
                THUGS = ThugData.read_all()
                for thug in THUGS:
                    if thug.exclusive:
                        exclusive += f"\n{Emoji.empty}{thug.emoji} {thug}"
                    elif thug.tier > 21:
                        elite += f"\n{Emoji.empty}{thug.emoji} {thug}"
                    else:
                        thugs += f"\n{Emoji.empty}{thug.emoji} {thug}"

                await interaction.followup.send(
                    embed=discord.Embed(
                        color=discord.Color.dark_blue(),
                        description=(
                            f"Total Thugs: {len(THUGS)}\nOVR Value: \u221E{thugs}{elite}{exclusive}"
                        ),
                    ).set_author(name=f"{member}", icon_url=member.avatar)
                )
            elif error_embed := self.bot.check_hunter(member, interaction):
                await interaction.followup.send(embed=error_embed)
            else:
                hunter = HunterData.read(member.id) or HunterData.create(member.id)
                THUGS = ThugData.read_all()
                XTHUGS = [thug for thug in THUGS if thug.exclusive]
                # gangRank = rank(id_=member.id, label="Gang")
                gang = hunter.gang

                gang_embed = discord.Embed(
                    color=discord.Color.dark_blue(),
                    description=(
                        f"Total Thugs: {gang.total}\nCollected: {gang.collected}/{len(THUGS)} "
                        f"({gang.x}/{len(XTHUGS)})\nOVR Value: {gang.value:n}\n"
                        # f"\nRank: {gangRank}"
                    ),
                ).set_author(name=member, icon_url=member.avatar)

                for rarity, thug_list in gang.all.items():
                    table = tabulate(
                        [
                            [
                                card.thug.name,
                                card.amount if card.amount != 0 else " ",
                                card.level,
                                card.power,
                            ]
                            for card in thug_list
                        ],
                        ["Name", "Amount", "Level", "Power"],
                        "presto",
                    )
                    gang_embed.description += f"\n**{Dot.rarity(rarity)}{rarity.capitalize()} ~ {len(thug_list)}**\n```{table}```"

                await interaction.followup.send(embed=gang_embed)
        except Exception as e:
            await self.error(e)
        else:
            await self.done()


async def setup(bot: commands.Bot):
    await bot.add_cog(Gang(bot))
