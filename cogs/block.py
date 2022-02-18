from discord.ext import commands

from .coordinate import Coordinate

class Block(commands.Cog):

    states = {'null': '🟥', 'empty': '⬛', 'blocked': '⬜',
        'occupied': '🏃', 'visited': '💩', 'end': '🚽'}

    def __init__(self, bot,
        coord: Coordinate,
        state: str = 'null'):
        
        self.bot = bot
        self.coord: Coordinate = coord
        self.state: str = state

    def __str__(self) -> str:
        return self.states[self.state]

    def __eq__(self, other) -> bool:
        return (self.coord == other.coord
                and self.state == other.state)
                
def setup(bot):
    bot.add_cog(Block(bot, Coordinate(-1, -1)))