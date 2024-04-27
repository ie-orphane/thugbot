import locale
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from utils import clr
from datetime import datetime, UTC
from models import HunterData


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="-", intents=discord.Intents.all())

    def log(self, type: str, name: str, message: str):
        log_time = clr.black(datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"))
        log_color = dict(
            {
                ("Info", clr.blue),
                ("Error", clr.red),
                ("Cog", clr.green),
                ("Task", clr.yellow),
            }
        )
        print(
            f"{log_time} {log_color.get(type, clr.cyan)(type)}     {clr.magenta(name)} {message}"
        )

    def check_hunter(
        self, member: discord.Member | discord.User, interaction: discord.Interaction
    ):
        if member.bot:
            errorEmbed = discord.Embed(
                color=discord.Color.red(),
                description=f"Unfortunately! {member.mention} can't be a **Hunter**.",
            )
            return errorEmbed

        if HunterData.read(member.id) is None and member.id != interaction.user.id:
            errorEmbed = discord.Embed(
                color=discord.Color.red(),
                description=f"{member.mention} is not a **Hunter** yet!\ninvite him to join us.",
            )
            return errorEmbed

    async def setup_hook(self: commands.Bot) -> None:
        initial_extensions = [
            "cogs." + command_file[:-3]
            for command_file in os.listdir("cogs")
            if command_file not in ["__pycache__", "__init__.py", "__schema__.py"]
        ]

        for extension in initial_extensions:
            await self.load_extension(extension)

        sync = await self.tree.sync()
        self.log("Info", "Cogs", f"{len(sync)} Slash Command(s) Synced")

    async def on_ready(self):
        self.log("Info", "Bot", f"Logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content.startswith(self.user.mention):
            await message.channel.send("I'm here!")

def main():
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    bot = Bot()
    if TOKEN:
        bot.run(TOKEN)
    else:
        bot.log("Error", "Bot", ".env missed TOKEN")

if __name__ == "__main__":
    # from test.main import main
    main()