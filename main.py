import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('[!]Dungeons are ready')

client.run('YOUR DISCORD BOT TOKEN')