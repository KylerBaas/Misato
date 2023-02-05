import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import giphy_client
from giphy_client.rest import ApiException
from random import seed, randint
import re

from modules.roulette.helper_functions import query_random_animemanga, generate_random_index 
from modules.roulette.variables import default_anime, default_manga

load_dotenv()
giphy_token = os.getenv('GIPHY_TOKEN')
giphy_instance = giphy_client.DefaultApi()

class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def gif(self, query: str, author):
        try:
            if query is None:
                query = "nothing"

            api_response = giphy_instance.gifs_search_get(giphy_token, query)
            data_set = api_response.data
            data_len = len(data_set)
            range = 30

            if(data_len < 30):
                range = data_len

            seed(None)
            rand_num = randint(0, range - 1)
            return author + " Here's a random " + query + " gif\n" f'{data_len[rand_num].images.fixed_height.url}'

        except ApiException as apie:
            print("Exception when calling DefaultApi")
        
    def anime_manga(self, media_type):
        if media_type == "ANIME":
            array = default_anime
            episode_type = 'episodes'
            msg_episode_type = 'Episode Count: '
            embed_colour = 0x109c48
        elif media_type == "MANGA":
            array = default_manga
            episode_type = 'chapters'
            msg_episode_type = 'Chapter Count: '
            embed_colour = 0x2367b0

        seed(None)
        rand_num = randint(0, 17000)

        received = query_random_animemanga(rand_num, media_type)

        # Original query failed, query for one of the anime/manga from default array so that 
        # an anime/manga can be dispalyed
        if received == False:
            default = generate_random_index(array)
            received = query_random_animemanga(default, media_type)

        anime_obj = received['data']['Media']

        # Assign the queried attributes to new variables to transform the data and avoid null values 
        title_english = anime_obj['title']['english'] if anime_obj['title']['english'] is not None else ""
        title_romaji = anime_obj['title']['romaji'] if anime_obj['title']['romaji'] is not None else ""
        average_score = str(anime_obj['averageScore']) + "%" if anime_obj['averageScore'] is not None else "N/A"
        episode_count = str(anime_obj[episode_type]) if ( anime_obj[episode_type] is not None ) else "N/A"
        anime_description = anime_obj['description'] if ( anime_obj['description'] is not None ) else "N/A"
        cover_image = anime_obj['coverImage']['large'] if ( anime_obj['coverImage']['large'] is not None ) else ""
        genres = anime_obj['genres'] if ( anime_obj['genres'] is not None ) else "N/A"

        # Build the embed object for displaying the anime/manga data
        embed = discord.Embed(
            title = title_english + " (" + title_romaji + ")" if title_english != "" and  title_english != title_romaji else title_romaji,  
            url = "https://anilist.co/" + mediaType.lower() + "/" + str(anime_obj['id']),
            description = "Average Score: " + average_score
                    + "\n" + msg_episode_type + episode_count 
                    + "\nGenres: " + ', '.join(genres)
                    + "\n\nDescription:\n" + re.sub("</*[a-z]+/*>*|href=", "", anime_description),
            colour = embed_colour 
        )
        embed.set_thumbnail(url = cover_image)
        return embed

    @commands.command()
    async def roulette(self, ctx, media_type: str, query: str = ""):
        content = ""
        media_type = media_type.upper()
        if media_type == "ANIME" or media_type == "MANGA":
            content = self.anime_manga(media_type)
            await ctx.send(embed = content)
        elif media_type == "GIF":
            content = self.gif(query, f'{ctx.author.mention}')
            await ctx.send(content)
        else:
            await ctx.send("After ::roulette, type in anime or manga or gif")
            return