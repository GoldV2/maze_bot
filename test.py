from logging import warning
from typing import Union

from discord.ext import commands
from discord import Message, NotFound
from discord.embeds import Embed
from discord.colour import Colour

class Coordinate(commands.Cog):

    def __init__(self, bot, i, j):
        self.bot = bot
        self.__i: int = i
        self.__j: int = j
    
    def down(self):
        return Coordinate(self.bot, self.__i-1, self.__j)

    def right(self):
        return Coordinate(self.bot, self.__i, self.__j+1)

    def left(self):
        return Coordinate(self.bot, self.__i, self.__j-1)

    def up(self):
        return Coordinate(self.bot, self.__i+1, self.__j)

def setup(bot):
    bot.add_cog(Coordinate(bot))