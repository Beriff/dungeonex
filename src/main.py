import discord
import game
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

control_messages = {}

def get_game_embed(user) -> discord.Embed:
    embed = discord.Embed(title='Dungeon Name', description=game.game_instances[user.name].get_printable(), color=0xffffff)
    embed.add_field(name='Last Action', value=game.game_instances[user.name].get_focused_entity().log, inline=True)
    embed.add_field(name='HP', value=game.game_instances[user.name].get_focused_entity().health, inline=True)
    embed.add_field(name='Level', value=game.game_instances[user.name].get_focused_entity().level, inline=True)
    embed.add_field(name='Exp', value=f'{game.game_instances[user.name].get_focused_entity().exp}/{game.game_instances[user.name].get_focused_entity().level**3}')    

    return embed

@client.event
async def on_ready():
    print('[!] Dungeons are ready')

@client.command()
async def newgame(ctx):
    newgame = game.Game(9, 8)
    newgame._generate_basic_grid()
    newgame.entities.append(game.rat_hero)
    newgame.entities.append(game.enemy)

    game.game_instances[ctx.author.name] = newgame

    print(f"[>] {ctx.author} issued .newgame")
    print(f"[>] {len(game.game_instances)} Game Instances are active")

    message = await ctx.send(embed=get_game_embed(ctx.author))

    control_messages[ctx.author.name] = message
    await control_messages[ctx.author.name].add_reaction('⬆')
    await control_messages[ctx.author.name].add_reaction('⬇')
    await control_messages[ctx.author.name].add_reaction('⬅')
    await control_messages[ctx.author.name].add_reaction('➡')

@client.event
async def on_reaction_add(reaction, user):
    if user.name != 'DungeonEx':
        try:
            if reaction.message.id == control_messages[user.name].id:
                if reaction.emoji == '⬆':
                    ctx = await client.get_context(reaction.message)
                    await moveup(ctx, user)
                    await reaction.message.remove_reaction('⬆', user)
                elif reaction.emoji == '⬇':
                    ctx = await client.get_context(reaction.message)
                    await movedown(ctx, user)
                    await reaction.message.remove_reaction('⬇', user)
                elif reaction.emoji == '⬅':
                    ctx = await client.get_context(reaction.message)
                    await moveleft(ctx, user)
                    await reaction.message.remove_reaction('⬅', user)
                elif reaction.emoji == '➡':
                    ctx = await client.get_context(reaction.message)
                    await moveright(ctx, user)
                    await reaction.message.remove_reaction('➡', user)

        except KeyError:
            print(f"[!] {user.name} tried to access foreign game")

async def moveup(ctx, user):
    active = game.game_instances[user.name]
    if active.move_focused_entity(0, -1):
        await ctx.message.edit(embed=get_game_embed(user))

async def movedown(ctx, user):
    active = game.game_instances[user.name]
    if active.move_focused_entity(0, 1):
        await ctx.message.edit(embed=get_game_embed(user))

async def moveleft(ctx, user):
    active = game.game_instances[user.name]
    if active.move_focused_entity(-1, 0):
        await ctx.message.edit(embed=get_game_embed(user))

async def moveright(ctx, user):
    active = game.game_instances[user.name]
    if active.move_focused_entity(1, 0):
        await ctx.message.edit(embed=get_game_embed(user))

client.run('TOKEN')
