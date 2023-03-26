import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import giphy_client
from giphy_client.rest import ApiException
from random import seed, randint
import re

from modules.roulette.helper_functions import query_anilist, generate_random_index, monthToString
from modules.roulette.variables import default_anime, default_manga

load_dotenv()
giphy_token = os.getenv('GIPHY_TOKEN')
giphy_instance = giphy_client.DefaultApi()


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def gif(self, search_term: str, author):
        try:
            if search_term is None:
                return "Enter a search term after gif"
            api_response = giphy_instance.gifs_search_get(
                giphy_token, search_term)
            data_set = api_response.data
            data_len = len(data_set)
            range = 30
            if (data_len < 30):
                range = data_len
            seed(None)
            rand_num = randint(0, range - 1)
            return author + " Here's a random " + search_term + " gif\n" f'{data_len[rand_num].images.fixed_height.url}'
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
        elif media_type == "CHARACTER":
            array = default_manga
            embed_colour = 0x2367b0

        seed(None)
        rand_num = randint(0, 17000)

        received = query_anilist(rand_num, media_type)

        # Original query failed, query for one of the anime/manga from default array so that
        # an anime/manga can be dispalyed
        if received == False:
            default = generate_random_index(array)
            received = query_anilist(default, media_type)

        if media_type == "ANIME" or media_type == "MANGA":
            anime_obj = received['data']['Media']
        elif media_type == "CHARACTER":
            anime_obj = received['data']['Character']

        title = ""
        image = ""
        description = ""

        if (media_type == "ANIME" or media_type == "MANGA"):
            # Assign the queried attributes to new variables to transform the data and avoid null values
            title_english = anime_obj['title']['english'] if anime_obj['title']['english'] is not None else ""
            title_romaji = anime_obj['title']['romaji'] if anime_obj['title']['romaji'] is not None else ""
            average_score = str(
                anime_obj['averageScore']) + "%" if anime_obj['averageScore'] is not None else "N/A"
            episode_count = str(anime_obj[episode_type]) if (
                anime_obj[episode_type] is not None) else "N/A"
            anime_description = anime_obj['description'] if (
                anime_obj['description'] is not None) else "N/A"
            image = anime_obj['coverImage']['large'] if (
                anime_obj['coverImage']['large'] is not None) else ""
            genres = anime_obj['genres'] if (
                anime_obj['genres'] is not None) else "N/A"

            title = title_english + \
                " (" + title_romaji + \
                ")" if title_english != "" and title_english != title_romaji else title_romaji
            description = "Average Score: " + average_score + "\n" + msg_episode_type + episode_count + "\nGenres: " + \
                ', '.join(genres) + "\n\nDescription:\n" + \
                re.sub("</*[a-z]+/*>*|href=", "", anime_description)

        elif (media_type == "CHARACTER"):
            title = anime_obj['name']['full'] if anime_obj['name']['full'] is not None else ""
            age = anime_obj['age'] if anime_obj['age'] is not None else "Unknown"
            birthday_year = anime_obj['dateOfBirth']['year'] if anime_obj['dateOfBirth']['year'] is not None else ""
            birthday_month = anime_obj['dateOfBirth']['month'] if anime_obj['dateOfBirth']['month'] is not None else ""
            birthday_day = anime_obj['dateOfBirth']['day'] if anime_obj['dateOfBirth']['day'] is not None else ""
            gender = anime_obj['gender'] if anime_obj['gender'] is not None else "Unknown"
            image = anime_obj['image']['large'] if (
                anime_obj['image']['large'] is not None) else ""
            char_description = anime_obj['description'] if (
                anime_obj['description'] is not None) else ""
            description = "Gender: " + gender + "\nBirthday: " + str(monthToString(birthday_month)) + " " + str(
                birthday_day) + " " + str(birthday_year) + "\nAge: " + age + "\n\nDescription:\n" + char_description

        # Build the embed object for displaying the data in discord
        embed = discord.Embed(
            title=title,
            url="https://anilist.co/" + media_type.lower() + "/" +
            str(anime_obj['id']),
            description=description,
            colour=embed_colour
        )
        embed.set_thumbnail(url=image)
        return embed

    @commands.command()
    async def roulette(self, ctx, media_type: str, search_term: str = ""):
        content = ""
        media_type = media_type.upper()
        if media_type == "ANIME" or media_type == "MANGA" or media_type == "CHARACTER":
            content = self.anime_manga(media_type)
            await ctx.send(embed=content)
        elif media_type == "GIF":
            content = self.gif(search_term, f'{ctx.author.mention}')
            await ctx.send(content)
        else:
            await ctx.send("After ::roulette, type in anime or manga or gif")
            return
