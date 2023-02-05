default_anime = [205, 101921, 30, 245, 170, 20057, 18679, 47, 20954, 199, 5680, 1, 7647, 11061]
default_manga = [31706, 30013, 30002, 30436, 54705, 34632, 30656, 30003]

anime_query = '''
    query ($id: Int, $search: String) {
        Media (id: $id, type: ANIME, isAdult: false, search: $search) {
            id
            title {
                romaji
                english
            }
            coverImage {
                large
            }
            description
            averageScore
            episodes
            genres
        }
    }
    '''
manga_query = '''
    query ($id: Int, $search: String) {
        Media (id: $id, type: MANGA, isAdult: false, search: $search) {
            id
            title {
                romaji
                english
            }
            coverImage {
                large
            }
            description
            averageScore
            chapters
            genres
        }
    }
    '''