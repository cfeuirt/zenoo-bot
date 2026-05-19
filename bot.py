import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

MOD_FILE = 'mods.json'

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
    print(f'Bot connecte : {bot.user}')

@bot.command()
@commands.has_permissions(administrator=True)
async def setmod(ctx, member: discord.Member, numero: int):
    mods = load_mods()
    mods[str(member.id)] = numero
    save_mods(mods)
    await ctx.send(f'Le moderateur {numero} a ete assigne.')

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
