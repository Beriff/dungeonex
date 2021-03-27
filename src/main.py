import discord
import game
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('[!] Dungeons are ready')

@client.command()
async def newgame(ctx):
    newgame = game.Game(7, 6)
    newgame._generate_basic_grid()
    newgame.entities.append(game.rat_hero)

    game.game_instances[ctx.author] = newgame

    print(f"[>] {ctx.author} issued .newgame")
    print(f"[>] {len(game.game_instances)} Game Instances are active")
    await ctx.send(game.game_instances[ctx.author].get_printable())

@client.command()
async def moveup(ctx):
    active = game.game_instances[ctx.author]
    if active.move_focused_entity(0, -1):
        print('passed')
    await ctx.send(game.game_instances[ctx.author].get_printable())

client.run('ODI1MjAyNTgxNjI1NTAzNzU0.YF6fyg.JVEDvweeB_mu51wx9HTaQumMeFU')
