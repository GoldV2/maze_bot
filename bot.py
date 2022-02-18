import os
import sys
from pathlib import Path

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), owner_id=250782339758555136,
                   intents=Intents.all(),)
                   # help_command=None)

path = Path(__file__).resolve().parent
if str(path) not in sys.path:
    sys.path.insert(1, str(path))

if __name__ == "__main__":
    cogs = {
    'cogs': ['coordinate', 'block', 'maze', 'game'],}

    for dir in cogs:
        for cog in cogs[dir]:
            bot.load_extension(f"{dir}.{cog}")

    load_dotenv()
    bot.run(os.getenv('DISCORD_SECRET'))