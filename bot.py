import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

MOD_FILE = 'mods.json'
GUILD_ID = 1506035311048917052
AUTOROLE_NAME = 'Membres'

def load_mods():
    if os.path.exists(MOD_FILE):
        with open(MOD_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_mods(mods):
    with open(MOD_FILE, 'w') as f:
        json.dump(mods, f)

@bot.event
async def on_ready():
    print(f'Bot 1 connecte : {bot.user}')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=AUTOROLE_NAME)
    if role:
        await member.add_roles(role)
        print(f'Role Membres donne a {member.name}')

@bot.command()
@commands.has_permissions(administrator=True)
async def setmod(ctx, member: discord.Member, numero: int):
    mods = load_mods()
    mods[str(member.id)] = numero
    save_mods(mods)
    await ctx.send(f'✅ Le moderateur {numero} a ete assigne a {member.name}')

@bot.command()
@commands.has_permissions(administrator=True)
async def getmod(ctx, member: discord.Member):
    mods = load_mods()
    numero = mods.get(str(member.id))
    if numero:
        await ctx.send(f'Le moderateur {numero}')
    else:
        await ctx.send(f'Aucun numero assigne.')

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
