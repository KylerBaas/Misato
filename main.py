import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Import the cogs from the modules
import modules.create.create as cog_create
import modules.roulette.roulette as cog_roulette

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='::')

# Add the cogs to the bot object so that the commands can be used
bot.add_cog(cog_create.Create(bot))
bot.add_cog(cog_roulette.Roulette(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

try:
    bot.run(discord_token)
except discord.errors.HTTPException and discord.errors.LoginFailure as e:
    print("Login unsuccessful.")