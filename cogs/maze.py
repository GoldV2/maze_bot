from random import choice

from discord.ext import commands

from .coordinate import Coordinate
from .block import Block

class Maze(commands.Cog):

    def __init__(self, bot, size: int = 10):
        self.bot = bot
        self.size = size if size < 14 else 14
        
        self.maze: list[list[Block]] = [[] for i in range(self.size)]
        self.blocks: dict[Coordinate, Block] = {}
        self.occupied: Coordinate = Coordinate(self.bot, i=0, j=0)

        self.generate()

    def generate(self) -> None:
        self.add_blocks()
        self.create_path()
        self.fill_maze()

    def add_blocks(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
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
        for block in self.blocks.values():
            if block.state == 'null':
                block.state = choice(['blocked', 'blocked', 'empty', 'empty', 'empty'])

        self.maze[0][0].state = 'occupied'
        self.maze[-1][-1].state = 'end'

    def move(self, direction: str) -> None:
        new_block = self.get_block(self.occupied.move(direction))
        if new_block and new_block.state != 'blocked':
            self.blocks[self.occupied].state = 'visited'
            new_block.state = 'occupied'
            self.occupied = new_block.coord

    def get_block(self, coord: Coordinate) -> Block:
        if coord in self.blocks:
            return self.blocks[coord]

    def poop(self) -> None:
        for block in self.blocks.values():
            if block.state == 'empty':
                block.state = 'visited'

    def __str__(self) -> str:
        s = ""
        for row in self.maze:
            for block in row:
                s += str(block)

            s += '\n'

        return s

def setup(bot):
    bot.add_cog(Maze(bot))