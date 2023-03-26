from random import seed, randint
import requests


def generate_random_index(array):
    size = len(array)
    seed(None)
    randNum = randint(0, size - 1)
    return array[randNum]


def query_anilist(rand_num, media_type: str):
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
    query_params = "$id: Int"

    if (media_type == "ANIME" or media_type == "MANGA"):
        episode_type = "episodes" if media_type == "ANIME" else "chapters"
        type_params = "Media(id: $id, type: {media_type}, isAdult: false)".format(
            media_type=media_type)
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
    elif (media_type == "CHARACTER"):
        type_params = "Character(id: $id)"
        field_params = '''
            id
            name {{
                full
            }}
            age
            image {{
                large
            }}
            dateOfBirth {{
                year
                month
                day
            }}
            description
            gender
        '''.format()

    query = '''
        query({query_params}) {{
            {type_params}{{
                {field_params}
            }}
        }}
    '''.format(query_params=query_params, type_params=type_params, field_params=field_params)
    return query


def monthToString(month: int):
    if (month is None):
        return ""
    if (month == 1):
        return "January"
    elif (month == 2):
        return "February"
    elif (month == 3):
        return "March"
    elif (month == 4):
        return "April"
    elif (month == 5):
        return "May"
    elif (month == 6):
        return "June"
    elif (month == 7):
        return "July"
    elif (month == 8):
        return "August"
    elif (month == 9):
        return "September"
    elif (month == 10):
        return "October"
    elif (month == 11):
        return "November"
    elif (month == 12):
        return "December"
