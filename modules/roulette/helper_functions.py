from random import seed, randint
import requests

def generate_random_index(array):
    size = len(array)
    seed(None)
    randNum = randint(0, size - 1)
    return array[randNum]


def query_animemanga(rand_num, media_type: str):
    query = build_query(media_type)
    variables = {
        'id': rand_num
    }
    url = 'https://graphql.anilist.co'

    try:
        response = requests.post(
            url, json={'query': query, 'variables': variables})
        if response.status_code == 404:
            return False
    except requests.exceptions.RequestException as e:
        return False
    return response.json()


def build_query(media_type: str):
    episode_type = "episodes" if media_type == "ANIME" else "chapters"
    query_params = "$id: Int"
    media_params = "id: $id, type: {type}, isAdult: false".format(type=media_type)
    field_params = '''
        id
        title {{
            romaji
            english
        }}
        coverImage {{
            large
        }}
        description
        averageScore
        {episode_type}
        genres
    '''.format(episode_type=episode_type)

    query = '''
        query({query_params}) {{
            Media({media_params}){{
                {field_params}
            }}
        }}
    '''.format(query_params=query_params, media_params=media_params, field_params=field_params)

    return query
