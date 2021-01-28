import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import Bot

import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

from random import seed, randint

from arrays import haikuLine1Array, haikuLine2Array, haikuLine3Array, animeArray, mangaArray, animeQuery, mangaQuery

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
    haikuLine1 = generateRandIndex(haikuLine1Array)
    haikuLine2 = generateRandIndex(haikuLine2Array)
    haikuLine3 = generateRandIndex(haikuLine3Array)

    haiku = haikuLine1 + "\n" + haikuLine2 + "\n" + haikuLine3
    await ctx.send(haiku)


@bot.command()
async def roulette(ctx, mediaType: str):
    # Make the type parameter uppercase
    mediaType = mediaType.upper()

    # Break out of command if the mediaType is not valid
    if mediaType != 'ANIME' and mediaType != 'MANGA':
        await ctx.send("After ::roulette, type in anime or manga")
        return

    # Generate random id number
    seed(None)
    randNum = randint(0, 120000)

    # Variable values for Anime
    array = animeArray
    episodeType = 'episodes'
    msgEpType = 'Episode Count: '
    embedColour = 0x109c48

    # Variable values for manga
    if mediaType == "MANGA":
        array = mangaArray
        episodeType = 'chapters'
        msgEpType = 'Chapter Count: '
        embedColour = 0x2367b0

    # Query for anime/manga object
    received = queryAnimeManga(randNum, mediaType)

    # Original query failed, query for one of the anime/manga from default array
    if received == False:
        default = generateRandIndex(array)
        received = queryAnimeManga(default, mediaType)

    # Object holding the retrieved data associated to the generated anime/manga id
    animeObj = received['data']['Media']

    # Check if any of the animeObj attributes are of NoneType, and set the value accordingly
    titleEnglish = animeObj['title']['english'] if animeObj['title']['english'] is not None else ""
    titleRomaji = animeObj['title']['romaji'] if animeObj['title']['romaji'] is not None else ""
    averageScore = str(animeObj['averageScore']) + "%" if animeObj['averageScore'] is not None else "N/A"
    episodeCount = str(animeObj[episodeType]) if ( animeObj[episodeType] is not None ) else "N/A"
    animeDescription = animeObj['description'] if ( animeObj['description'] is not None ) else "N/A"
    coverImage = animeObj['coverImage']['medium'] if ( animeObj['coverImage']['medium'] is not None ) else "https://i.redd.it/su8274uv8zh11.jpg"

    # Build the embed object for displaying the data
    embed = discord.Embed(
        title = titleEnglish + " (" + titleRomaji + ")" if titleEnglish != "" else titleRomaji,  
        url = "https://anilist.co/anime/" + str(animeObj['id']),
        description = "Average Score: " + averageScore
                    + "\n" + msgEpType + episodeCount 
                    + "\n\nDescription:\n" + animeDescription,
        colour = 0x33cc33 
    )
    # Set the cover image as the thumbnail image of the embed
    embed.set_thumbnail(url = coverImage)

    # Send the embed
    await ctx.send(embed = embed)


##################################################################################################################################################################


###################################################### HELPER FUNCTIONS ######################################################

# Queries for anime/manga data from randomly generated id
def queryAnimeManga(randNum, mediaType):
    # GraphQL query for anime/manga data based on the generated id 
    query = animeQuery if mediaType == "ANIME" else mangaQuery
    #
    variables = {
        'id': randNum
    }
    # Link to anilist
    url = 'https://graphql.anilist.co'

    try:
        # Make an HTTP API request
        response = requests.post(url, json = {'query': query, 'variables': variables})
        # Queried id does not exist, return false
        if response.status_code == 404:
            return False

    # Error in query, return false
    except requests.exceptions.RequestException as e:
        return False

    # No errors, return with queried data in JSON format
    return response.json()


# Generates a random number as an index in an array
def generateRandIndex(array):
    # Size of the array
    size = len(array)
    # Generate random number within the range of the array size
    seed(None)
    randNum = randint(0, size - 1)

    return array[randNum]


##################################################################################################################################################################

# Main execution of bot
try:
    bot.run(discordToken)
except discord.errors.HTTPException and discord.errors.LoginFailure as e:
    print("Login unsuccessful.")