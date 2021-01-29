haikuLine1Array = ["big", "small"]
haikuLine2Array = ["large", "tiny"]
haikuLine3Array = ["giant", "microscopic"]

animeArray = [205, 101921, 30, 245, 170, 20057, 18679, 47, 20954, 199, 5680, 1, 7647, 11061]
mangaArray = [31706, 30013, 30002, 30436, 54705, 34632, 30656, 30003]

animeQuery = '''
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
            }
            coverImage {
                medium
            }
            description
            averageScore
            episodes
        }
    }
    '''
mangaQuery = '''
    query ($id: Int) {
        Media (id: $id, type: MANGA) {
            id
            title {
                romaji
                english
            }
            coverImage {
                medium
            }
            description
            averageScore
            chapters
        }
    }
    '''