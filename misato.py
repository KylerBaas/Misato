import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import Bot

import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

import random
from random import seed
from random import randint

import math


load_dotenv()

#intents = discord.Intents.default()
#intents.members = True

# Discord Token
discordToken = os.getenv('DISCORD_TOKEN')
# Giphy token
giphyToken = os.getenv('GIPHY_TOKEN')


apiInstance = giphy_client.DefaultApi()

# Bot object
bot = commands.Bot(command_prefix='::')


################# Event Listeners #################

# Event listener for when bot has connected
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def yo(ctx):
    await ctx.reply("Yo whattup")
    
        
@bot.command()
async def gif(ctx, query: str):
    await ctx.send("Here's a random " + query + " gif for you")
    try:
        apiResponse = apiInstance.gifs_search_get(giphyToken, query)
        dataSet = apiResponse.data
        dataLen = len(dataSet)
        print(dataLen)
        range = 30

        # Check if the length of the dataset is shorter than the default search range of 30
        if(dataLen < 30):
            range = dataLen

        # Generate a seed and random number for selecting the gif
        seed(None)
        randNum = randint(0, range)
        # Display the gif selected from the data set
        await ctx.send(dataSet[randNum].images.fixed_height.url)

    # Handle an ApiException related to the Giphy API
    except ApiException as apie:
        print("Exception when calling DefaultApi")

@bot.command()
async def haiku(ctx):
    haikus = ["big", "samll"]
    seed(None)
    randNum = randint(0, 2)
    ctx.send(haikus[randNum])


@bot.command()
async def calc(ctx, num1: float, op, num2: float):
    if num1 != None and op != None and num2 != None: 
        await ctx.send("The answer is: ")
        if op == '+':
            await ctx.send(num1 + num2)
        elif op == '-':
            await ctx.send(num1 - num2)
        elif op == '*':
            await ctx.send(num1 * num2)
        elif op == '^':
            await ctx.send(num1 ** num2)
        else:
            await ctx.send("Invalid operator!")
    else:
        await ctx.send("Invalid format!")


try:
    bot.run(discordToken)
except discord.errors.HTTPException and discord.errors.LoginFailure as e:
    print("Login unsuccessful.")