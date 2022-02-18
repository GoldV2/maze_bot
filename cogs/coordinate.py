from discord.ext import commands

class Coordinate(commands.Cog):
    def __init__(self, bot, i: int = -1, j: int = -1):
        self.bot = bot
        self.i: int = i
        self.j: int = j
    
    def move(self, direction: str):
        if direction == 'down':
            return Coordinate(self.bot, self.i, self.j+1)

        elif direction == 'right':
            return Coordinate(self.bot, self.i+1, self.j)

        elif direction == 'left':
            return Coordinate(self.bot, self.i-1, self.j)

        elif direction == 'up':
            return Coordinate(self.bot, self.i, self.j-1)

    def __eq__(self, other) -> bool:
        return self.i == other.i and self.j == other.j

    def __hash__(self) -> hash:
        return hash((self.__class__, self.i, self.j))

def setup(bot):
    bot.add_cog(Coordinate(bot))