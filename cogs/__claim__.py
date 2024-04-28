import discord
from discord.ext import commands
from models import HunterData
from cogs import Cog


class Claim(Cog):
    @discord.app_commands.command(description="Get a new thug for your gang")
    async def claim(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            self.interaction = interaction
            self.start()

            hunter = HunterData.read(interaction.user.id) or HunterData.create(
                interaction.user.id
            )
            onCooldown, time = hunter.check_cooldown("claim")

            if onCooldown:
                await interaction.followup.send(
                    embed=discord.Embed(
                        color=discord.Color.red(),
                        description=f"{interaction.user.mention}\nYou are on cooldown for this command!\nNext available in {time}",
                    ),
                    ephemeral=True,
                )

            else:
                card = hunter.claim_thug()
                await interaction.followup.send(
                    file=discord.File(fp=card.thug.path, filename=card.thug.file_name),
                    embed=discord.Embed(
                        color=card.color,
                        description=f"**{card.thug.name}** joins your gang",
                    ).set_image(url=f"attachment://{card.thug.file_name}"),
                )
        except Exception as e:
            await self.error(e)
        else:
            await self.done()


async def setup(bot: commands.Bot):
    await bot.add_cog(Claim(bot))
