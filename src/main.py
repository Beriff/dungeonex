import discord
import game
from discord.ext import commands
from copy import deepcopy

client = commands.Bot(command_prefix = '.')

control_messages = {}

enemies = {"monkey": game.enemy}

def get_game_embed(user) -> discord.Embed:
    embed = discord.Embed(title=game.game_instances[user.name].dungeon_name + ' dungeon', description=game.game_instances[user.name].get_printable(), color=0xffffff)
    embed.add_field(name='Last Action', value=game.game_instances[user.name].get_focused_entity().log, inline=True)
    embed.add_field(name='HP', value=game.game_instances[user.name].get_focused_entity().health, inline=True)
    embed.add_field(name='Level', value=game.game_instances[user.name].get_focused_entity().level, inline=True)
    embed.add_field(name='Exp', value=f'{game.game_instances[user.name].get_focused_entity().exp}/{game.game_instances[user.name].get_focused_entity().level**3}')    

    return embed

async def end_game(ctx, user) -> None:
    await control_messages[user.name].delete()
    del(control_messages[user.name])
    del(game.game_instances[user.name])

    print(f'[!] {user.name} game ended')
    print(f"[>] {len(game.game_instances)} Game Instances are active")

    await ctx.send('Game over!')

async def show_inv(ctx, user) -> None:
    game.game_instances[user.name].focused_window = int(not bool(game.game_instances[user.name].focused_window))
    await ctx.message.edit(embed=get_game_embed(user))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=".info"))
    print('[!] Dungeons are ready')

@client.command()
async def newgame(ctx):
    if ctx.author.name in game.game_instances:
        return False
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
    await control_messages[ctx.author.name].add_reaction('⬅')    
    await control_messages[ctx.author.name].add_reaction('⬇')
    await control_messages[ctx.author.name].add_reaction('➡')
    await control_messages[ctx.author.name].add_reaction('⏺')

@client.command()
async def control(ctx, username, command, param_a):
    active = game.game_instances[username]
    if command == "add":
        active.entities.append(deepcopy(enemies[param_a]))
        await ctx.send('Executed')

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
                elif reaction.emoji == '⏺':
                    ctx = await client.get_context(reaction.message)
                    await show_inv(ctx, user)
                    await reaction.message.remove_reaction('⏺', user)


        except KeyError:
            print(f"[!] {user.name} tried to access foreign game")
        except:
            pass

@client.command()
async def endgame(ctx):
    print(f"[>] {ctx.author} issued .endgame")
    await end_game(ctx, ctx.author)

async def moveup(ctx, user):
    active = game.game_instances[user.name]
    if active.move_focused_entity(0, -1):
        if active.get_focused_entity().health <= 0:
            await end_game(ctx, user)
        else:
            await ctx.message.edit(embed=get_game_embed(user))

async def movedown(ctx, user):
    active = game.game_instances[user.name]
    if active.move_focused_entity(0, 1):
        if active.get_focused_entity().health <= 0:
            await end_game(ctx, user)
        else:
            await ctx.message.edit(embed=get_game_embed(user))

async def moveleft(ctx, user):
    active = game.game_instances[user.name]
    if active.move_focused_entity(-1, 0):
        if active.get_focused_entity().health <= 0:
            await end_game(ctx, user)
        else:
            await ctx.message.edit(embed=get_game_embed(user))

async def moveright(ctx, user):
    active = game.game_instances[user.name]
    if active.move_focused_entity(1, 0):
        if active.get_focused_entity().health <= 0:
            await end_game(ctx, user)
        else:
            await ctx.message.edit(embed=get_game_embed(user))

client.run('TOKEN')
