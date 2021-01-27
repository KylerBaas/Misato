import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import Bot

import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

from random import seed, randint

from arrays import haikuLine1Array, haikuLine2Array, haikuLine3Array, animeArray

import requests

load_dotenv()


# Discord Token
discordToken = os.getenv('DISCORD_TOKEN')
# Giphy token
giphyToken = os.getenv('GIPHY_TOKEN')


apiInstance = giphy_client.DefaultApi()

# Bot object
bot = commands.Bot(command_prefix='::')


###################################################### EVENT LISTENERS ######################################################

# Event listener for when bot has connected
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# Event listener for displaying gifs from giphy        
@bot.command()
async def gif(ctx, query: str = None):
    try:
        if query is None:
            query = "nothing"

        apiResponse = apiInstance.gifs_search_get(giphyToken, query)
        dataSet = apiResponse.data
        dataLen = len(dataSet)
        range = 30

        # Check if the length of the dataset is shorter than the default search range of 30
        if(dataLen < 30):
            range = dataLen

        # Generate a seed and random number for selecting the gif
        seed(None)
        randNum = randint(0, range - 1)
        # Display the gif selected from the data set along with the message
        await ctx.send(f'{ctx.author.mention}' " Here's a random " + query + " gif\n" f'{dataSet[randNum].images.fixed_height.url}')

    # Handle an ApiException related to the Giphy API
    except ApiException as apie:
        print("Exception when calling DefaultApi")



@bot.command()
async def haiku(ctx):

    # Retrieve three lines for the haiku
    haikuLine1 = generateRandNum(haikuLine1Array)
    haikuLine2 = generateRandNum(haikuLine2Array)
    haikuLine3 = generateRandNum(haikuLine3Array)

    haiku = haikuLine1 + "\n" + haikuLine2 + "\n" + haikuLine3
    await ctx.send(haiku)



@bot.command()
async def animeroulette(ctx):
    seed(None)
    randNum = randint(0, 120000)

    received = queryAnime(randNum)

    # If the original query failed, query for one of the anime
    if received == False:
        defaultAnime = generateRandNum(animeArray)
        received = queryAnime(defaultAnime)

    anime = received['data']['Media']

    embed = discord.Embed(
        title = anime['title']['romaji'], 
        url = "https://anilist.co/anime/" + str(anime['id']),
        description = "\"*Forrest Gump mama said, Life is like a box of chocolates (You never know what you're gonna get)*\"\n - Kanye West"
    )
    embed.set_image(url="https://i.redd.it/su8274uv8zh11.jpg")
    await ctx.send(embed = embed)


##################################################################################################################################################################


###################################################### HELPER FUNCTIONS ######################################################

def queryAnime(randNum):
   # Query for 
    query = '''
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
            }
        }
    }'''

    variables = {
        'id': randNum
    }

    url = 'https://graphql.anilist.co'

    try:
        # Make an HTTP API request
        response = requests.post(url, json = {'query': query, 'variables': variables})
        
        # Queried 
        if response.status_code == 404:
            return False
    # Error in query, return with false
    except requests.exceptions.RequestException as e:
        return False

    return response.json()


# Generates a random number as an index in an array
def generateRandNum(array):
    size = len(array)
    seed(None)
    randNum = randint(0, size - 1)
    return array[randNum]

##################################################################################################################################################################

# Main execution of bot
try:
    bot.run(discordToken)
except discord.errors.HTTPException and discord.errors.LoginFailure as e:
    print("Login unsuccessful.")