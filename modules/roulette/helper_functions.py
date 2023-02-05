from random import seed, randint
import requests

# Import the defined GraphQL queries used for requesting anime/manga records
from modules.roulette.variables import anime_query, manga_query

def generate_random_index(array):
    size = len(array)
    seed(None)
    randNum = randint(0, size - 1)
    return array[randNum]

def query_random_animemanga(randNum, mediaType):
    query = anime_query if mediaType == "ANIME" else manga_query
    variables = {
        'id': randNum
    }
    url = 'https://graphql.anilist.co'

    try:
        response = requests.post(url, json = {'query': query, 'variables': variables})
        if response.status_code == 404:
            return False
    except requests.exceptions.RequestException as e:
        return False
    return response.json()