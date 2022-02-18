import asyncio

import discord
from discord.ext import commands

from .maze import Maze

class Game(commands.Cog):

    def __init__(self, bot):        
        self.bot = bot
        self.maze_channel: int = None

    @commands.command()
    @commands.is_owner()
    async def maze_here(self, ctx):
        self.maze_channel = ctx.channel    

    @commands.command()
    async def maze(self, ctx, p2) -> None:
        def sent_in_maze_channel(ctx):
            return ctx.channel == self.maze_channel

        if sent_in_maze_channel(ctx):
            p1_info = {'player': None, 'msg': None}
            p2_info = {'player': None, 'msg': None}
            
            p1 = ctx.author
            p1_info['player'] = p1

            p2_id = p2[2:-1]
            if '!' in p2_id:
                p2_id = p2_id.replace('!', '')
            p2 = ctx.guild.get_member(int(p2_id))
            p2_info['player'] = p2
            
            m1 = Maze(self.bot, 10, 10)
            m1.generate()
            m2 = Maze(self.bot, 10, 10)
            m2.generate()

            v1 = GameView(p1, m1)
            v2 = GameView(p2, m2)

            accept_view = AcceptView()
            await p2.send("You hear fast small steps in the middle of the night, seems like someone is going to the bathroom, and fast... You suddenly feel an urge to poop.",
                view=accept_view)
            await accept_view.wait()
            if accept_view.accepted:
                await p1.send("You hear someone getting up. You pick up your pace to make sure you get to the bathroom!")
                msg1 = await p1.send(str(m1), view=v1)
                msg2 = await p2.send(str(m2), view=v2)
                p1_info['msg'] = msg1
                p2_info['msg'] = msg2

                done, pending = await asyncio.wait([
                    asyncio.create_task(v1.wait(), name='v1'),
                    asyncio.create_task(v2.wait(), name='v2')
                ], return_when=asyncio.FIRST_COMPLETED)
                first = done.pop()

                v1.stop()
                v2.stop()

                if first.get_name() == 'v1':
                    winner = p1_info
                    loser = p2_info
                else:
                    winner = p2_info
                    loser = p1_info

                won_message = 'Congratulations, you made it to the bathroom first!'
                lost_message = 'You pooped your pants, someone else got to the bathroom first!'
                await winner['msg'].edit(content=won_message, view=None)
                await loser['msg'].edit(content=lost_message, view=None)

                await ctx.send(f"{winner['player'].nick} got to the bathroom before {loser['player'].nick}, who unfortunately pooped his pants!")

            else:
                await p1.send(f"Luckily you were quiet enough and did not wake up {p2.nick}, you have the bathroom all to yourself.")

class GameView(discord.ui.View):
    def __init__(self, p: discord.Member, maze: Maze):
        super().__init__(timeout=None)
        
        self.p: discord.Member = p
        self.maze: Maze = maze

    @discord.ui.button(label='Up', style=discord.ButtonStyle.blurple)
    async def up(self, button, interaction):
        new_coord = self.maze.blocks[self.maze.occupied].coord.move('up')
        if new_coord in self.maze.blocks and self.maze.blocks[new_coord].state != 'blocked':
            self.maze.blocks[self.maze.occupied].state = 'visited'
            self.maze.occupied = new_coord
            self.maze.blocks[self.maze.occupied].state = 'occupied'

            await interaction.response.edit_message(content=str(self.maze))

            self.won()

    @discord.ui.button(label='Down', style=discord.ButtonStyle.blurple, row=2)
    async def down(self, button, interaction):
        new_coord = self.maze.blocks[self.maze.occupied].coord.move('down')
        if new_coord in self.maze.blocks and self.maze.blocks[new_coord].state != 'blocked':
            self.maze.blocks[self.maze.occupied].state = 'visited'
            self.maze.occupied = new_coord
            self.maze.blocks[self.maze.occupied].state = 'occupied'

            await interaction.response.edit_message(content=str(self.maze))

            self.won()

    @discord.ui.button(label='Left', style=discord.ButtonStyle.blurple)
    async def left(self, button, interaction):
        new_coord = self.maze.blocks[self.maze.occupied].coord.move('left')
        if new_coord in self.maze.blocks and self.maze.blocks[new_coord].state != 'blocked':
            self.maze.blocks[self.maze.occupied].state = 'visited'
            self.maze.occupied = new_coord
            self.maze.blocks[self.maze.occupied].state = 'occupied'

            await interaction.response.edit_message(content=str(self.maze))

            self.won()

    @discord.ui.button(label='Right', style=discord.ButtonStyle.blurple, row=2)
    async def right(self, button, interaction):
        new_coord = self.maze.blocks[self.maze.occupied].coord.move('right')
        if new_coord in self.maze.blocks and self.maze.blocks[new_coord].state != 'blocked':
            self.maze.blocks[self.maze.occupied].state = 'visited'
            self.maze.occupied = new_coord
            self.maze.blocks[self.maze.occupied].state = 'occupied'

            await interaction.response.edit_message(content=str(self.maze))

            self.won()

    def won(self):
        if self.maze.maze[-1][-1].state == 'occupied':
            self.stop()

class AcceptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        self.accepted = False

    @discord.ui.button(label='Wake Up', style=discord.ButtonStyle.green)
    async def accept(self, button, interaction):
        self.accepted = True
        self.stop()
        await interaction.response.edit_message(content="As you get up from the bed, the steps get louder and faster... You have to get up quick and run to the bathroom!",view=None)

    @discord.ui.button(label='Hold it In', style=discord.ButtonStyle.red, row=2)
    async def refuse(self, button, interaction):
        self.stop()
        await interaction.response.edit_message(content="You remembered you have diapers on, so you decide to go back to sleep.",view=None)

def setup(bot):
    bot.add_cog(Game(bot))