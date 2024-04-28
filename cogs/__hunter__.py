import discord
from discord.ext import commands
from models import Emoji
from typing import Optional
from models import HunterData
from cogs import Cog


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


class Hunter(Cog):
    @discord.app_commands.command(description="Get information about a Thug Hunter")
    async def hunter(
        self, interaction: discord.Interaction, member: Optional[discord.Member] = None
    ):
        try:
            await interaction.response.defer()
            self.interaction = interaction
            self.start()
            member = member or interaction.user

            if member.id == 1063459223289200652:
                await interaction.followup.send(embed=HunterEmbed(member=member))
            elif error_embed := self.bot.check_hunter(member, interaction):
                await interaction.followup.send(embed=error_embed)
            else:
                hunter = HunterData.read(member.id) or HunterData.create(member.id)

                await interaction.followup.send(
                    embed=HunterEmbed(
                        member=member,
                        highLevel=hunter.level >= 69,
                        level=f"**{hunter.level:n}**",
                        xp=f"**{hunter.xp:n}** / {hunter.required_xp():n}",
                        coins=f"**{hunter.coin:n}**",
                        stars=f"**{hunter.star:n}**",
                    )
                )
        except Exception as e:
            await self.error(e)
        else:
            await self.done()


async def setup(bot: commands.Bot):
    await bot.add_cog(Hunter(bot))
