from disnake.ext import commands
from disnake import Intents
from os import listdir
from disnake import Embed, Color
from random import randint
import datetime
import disnake
from asyncio import sleep


intents = Intents.default()
intents.integrations = True
intents.voice_states = True
intents.members = True
intents.guilds = True


bot = commands.InteractionBot(intents=intents)

@bot.event
async def on_ready():
    for file in listdir("cogs/"):
        if file.endswith(".py"):
            bot.load_extension(f"cogs.{file[:-3]}")

    print("ready")

@bot.event
async def on_member_join(member):
    welcome = Embed(title="Welcome!", description="Welcome to Impossible, Make sure you read the rules and have a great time, dont feel scared to dm the owner with questions or concerns", color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    now = datetime.datetime.now()
    now = now.strftime("%b %d %Y")
    log = Embed(title=f"{member} joined on {now}", description="This member just joined the server", color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    log.add_field(name="joined discord on", value=member.created_at.strftime("%b %d %Y"))

    log_channel = disnake.utils.get(member.guild.channels, id=989016380437307403)
    await log_channel.send(embed=log)
    await member.send(embed=welcome)

@bot.slash_command(description="Displays information about a user")
async def whois(inter, user:disnake.Member):
    title = f"{user} ({user.id}"
    description = f"{user} joined on {user.joined_at.strftime('%b %d %Y')}, and created their account on {user.created_at.strftime('%b %d %Y')}"
    highest_role = user.roles[-1]
    is_owner = user.guild.owner_id == user.id

    emb = Embed(title=title, description=description, color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    emb.add_field(name="highest role", value=highest_role)
    emb.set_thumbnail(url=user.avatar.url)
    emb.add_field(name="Is owner", value=is_owner)
    await inter.response.send_message(embed=emb)

@bot.slash_command(description="purges a specified number of messages")
@commands.has_permissions(manage_messages=True)
async def purge(inter, limit:int, channel:disnake.channel.TextChannel=None):
    if channel == None:
        channel = inter.channel

    await channel.purge(limit=limit)
    message = await channel.send(f"{inter.author} cleared {limit} messages")
    
@purge.error
async def on_purge_error(inter, error):
    print(error)
    if isinstance(error, commands.MissingPermissions):
        await inter.response.send_message(embed=Embed(title=f"You are missing {','.join(error.missing_permissions)} permission", color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255))))
    
    if isinstance(error, commands.BotMissingPermissions):
        await inter.response.send_message(embed=Embed(f"I am missing {','.join(error.missing_permissions)} permissions", color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255))))

@bot.slash_command(description="manages a users roles")
@commands.has_permissions(administrator=True)
async def manageroles(inter, user:disnake.Member, role:disnake.Role, operation:str=commands.Param(choices=["add", "remove"])):
    if operation == "add":
        await user.add_roles(role)
        await inter.response.send_message(embed=Embed(title="Added role", color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255))))
    else:
        if role in user.roles:
            await user.remove_roles(role)
            await inter.response.send_message(embed=Embed(title="Removed role", color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255))))
        else:
            await inter.response.send_message(embed=Embed(title="Cannot remove a role the user doesnt have!", color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255))))

@manageroles.error
async def onManageError(inter, error):
    await on_purge_error(inter, error)


bot.run("TOKEN")
