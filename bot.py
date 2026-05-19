import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

MOD_FILE = 'mods.json'
AUTOROLE_FILE = 'autorole.json'

def load_mods():
    if os.path.exists(MOD_FILE):
        with open(MOD_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_mods(mods):
    with open(MOD_FILE, 'w') as f:
        json.dump(mods, f)

def load_autorole():
    if os.path.exists(AUTOROLE_FILE):
        with open(AUTOROLE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_autorole(data):
    with open(AUTOROLE_FILE, 'w') as f:
        json.dump(data, f)

@bot.event
async def on_ready():
    print(f'Bot connecte : {bot.user}')

@bot.event
async def on_member_join(member):
    data = load_autorole()
    role_id = data.get(str(member.guild.id))
    if role_id:
        role = member.guild.get_role(int(role_id))
        if role:
            await member.add_roles(role)

@bot.command()
@commands.has_permissions(administrator=True)
async def autorole(ctx, role: discord.Role):
    data = load_autorole()
    data[str(ctx.guild.id)] = str(role.id)
    save_autorole(data)
    await ctx.send(f'✅ Le rôle **{role.name}** sera donné automatiquement aux nouveaux membres !')

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
