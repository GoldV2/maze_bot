from random import choice

from discord.ext import commands

from .coordinate import Coordinate
from .block import Block

class Maze(commands.Cog):

    def __init__(self, bot, height: int, width: int):
        self.bot = bot
        self.height: int = height
        self.width: int = width
        self.maze: list[list[Block]] = [[] for i in range(height)]
        self.blocks: dict[Coordinate, Block] = {}
        self.occupied: Coordinate = Coordinate(self.bot, i=0, j=0)

    def generate(self) -> None:
        self.add_blocks()
        self.create_path()
        self.fill_maze()

    def add_blocks(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                coord = Coordinate(self.bot, i=i, j=j)
                block = Block(self.bot, coord)
                self.maze[j].append(block)
                self.blocks[coord] = block

    def create_path(self) -> None:
        current = self.maze[0][0]
        current.state = 'empty'
        while current != self.maze[-1][-1]:
            direction = choice(['down', 'right'])
            coord = current.coord.move(direction)
            if coord in self.blocks:
                current = self.blocks[coord]
                self.blocks[coord].state = 'empty'

    def fill_maze(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j].state == 'null':
                    state = choice(['blocked', 'blocked', 'empty', 'empty', 'empty'])
                    self.maze[i][j].state = state

        self.maze[0][0].state = 'occupied'
        self.maze[-1][-1].state = 'end'

    def get(self, coord: Coordinate) -> Block:
        return self.blocks[coord]

    def __str__(self) -> str:
        s = ""
        for row in self.maze:
            for block in row:
                s += str(block)

            s += '\n'

        return s

def setup(bot):
    bot.add_cog(Maze(bot, -1, -1))
