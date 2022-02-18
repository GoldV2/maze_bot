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
    async def here(self, ctx):
        self.maze_channel = ctx.channel    

    @commands.command()
    async def maze(self, ctx, p2: str, size: str) -> None:
        def sent_in_maze_channel(ctx):
            return ctx.channel == self.maze_channel

        if sent_in_maze_channel(ctx):
            p1_info = {}
            p2_info = {}
            
            # getting player 1
            p1 = ctx.author
            p1_info['player'] = p1

            # getting player 2
            p2_id = p2[2:-1]
            if '!' in p2_id:
                p2_id = p2_id.replace('!', '')
            p2 = ctx.guild.get_member(int(p2_id))
            p2_info['player'] = p2
            
            # creating mazes
            if size:
                m1 = Maze(self.bot, size=int(size))
                m2 = Maze(self.bot, size=int(size))

            else:
                m1 = Maze(self.bot)
                m2 = Maze(self.bot)

            p1_info['maze'] = m1
            p2_info['maze'] = m2

            # asking player two if they want to play
            accept_view = AcceptView()
            await p2.send("You hear fast small steps in the middle of the night, seems like someone is going to the bathroom, and fast... You suddenly feel an urge to poop.",
                view=accept_view)
            await accept_view.wait()
            if accept_view.accepted:
                await p1.send("You hear someone getting up. You pick up your pace to make sure you get to the bathroom!")
                
                # creating games views
                v1 = GameView(p1, m1)
                v2 = GameView(p2, m2)
                
                # sending game views to users
                msg1 = await p1.send(str(m1), view=v1)
                msg2 = await p2.send(str(m2), view=v2)
                p1_info['msg'] = msg1
                p2_info['msg'] = msg2

                # waiting for someone to be done
                done, pending = await asyncio.wait([
                    asyncio.create_task(v1.wait(), name='v1'),
                    asyncio.create_task(v2.wait(), name='v2')
                ], return_when=asyncio.FIRST_COMPLETED)
                first = done.pop()

                await v1.disable(msg1)
                await v2.disable(msg2)

                # deterining who won
                if first.get_name() == 'v1':
                    winner = p1_info
                    loser = p2_info
                else:
                    winner = p2_info
                    loser = p1_info

                # pooping everywhere
                loser['maze'].poop()
                await loser['msg'].edit(content=str(loser['maze']))

                # sending messages
                won_message = 'Congratulations, you made it to the bathroom first!'
                lost_message = 'You pooped your pants, someone else got to the bathroom first!'
                await winner['player'].send(content=won_message)
                await loser['player'].send(content=lost_message)

                # sending messages to the original channel
                await ctx.send(f"{winner['player'].nick} got to the bathroom before {loser['player'].nick}, who unfortunately pooped his pants!\n\nGame Stats")
                await ctx.send(f"{winner['player'].nick}'s Maze\n{winner['maze']}")
                await ctx.send(f"{loser['player'].nick}'s Maze (of course it has poop everywhere)\n{loser['maze']}")

            else:
                await p1.send(f"Luckily you were quiet enough and did not wake up {p2.nick}, you have the bathroom all to yourself.")

class GameView(discord.ui.View):
    def __init__(self, p: discord.Member, maze: Maze):
        super().__init__(timeout=None)
        
        self.p: discord.Member = p
        self.maze: Maze = maze

        directions = [('up', 1), ('down', 2), ('left', 1), ('right', 2)]
        for direction, row in directions:
            self.add_item(DirectionButton(direction, row))

    def won(self):
        if self.maze.maze[-1][-1].state == 'occupied':
            self.stop()

    async def disable(self, msg):
        self.stop()

        for child in self.children:
            child.disabled = True

        await msg.edit(view=self)

class DirectionButton(discord.ui.Button):
    def __init__(self, direction: str, row: int):
        super().__init__(style=discord.ButtonStyle.blurple,
            label=direction.capitalize(),
            row=row)

        self.direction = direction

    async def callback(self, interaction):
        self.view.maze.move(self.direction)
        await interaction.response.edit_message(content=str(self.view.maze))
        self.view.won()

class AcceptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        self.accepted = False

    @discord.ui.button(label='Wake Up', style=discord.ButtonStyle.green)
    async def accept(self, button, interaction):
        self.accepted = True
        await self.stop(interaction)
        await interaction.response.send_message(content="As you get up from the bed, the steps get louder and faster... You have to get up quick and run to the bathroom!")

    @discord.ui.button(label='Hold it In', style=discord.ButtonStyle.red, row=2)
    async def refuse(self, button, interaction):
        await self.stop(interaction)
        await interaction.response.send_message(content="You remembered you have diapers on, so you decide to go back to sleep.")

    async def stop(self, interaction):
        super().stop()

        for child in self.children:
            child.disabled = True

        await interaction.message.edit(view=self)

def setup(bot):
    bot.add_cog(Game(bot))