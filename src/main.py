import discord
import game
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('[!]Dungeons are ready')

@client.command()
async def newgame(ctx):
    newgame = game.Game(7, 5)
    newgame._generate_basic_grid()
    print(f"[>]{ctx.author} issued .newgame")
    await ctx.send(newgame.get_printable())

client.run('TOKEN')
