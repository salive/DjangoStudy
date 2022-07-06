from urllib import response
import requests
import json


API_KEY = '22f7c6de-6224-4f2b-a718-ef79627c526a'
URLS = ['https://kinopoiskapiunofficial.tech/api/v2.1/films/',
        'https://kinopoiskapiunofficial.tech/api/v2.2/films/']
HEADERS = {
    'X-API-KEY': API_KEY
}


class KPResponse:
    def __init__(self, kinopoisk_id, title_ru, title_en, year, poster, rating,  description, type):
        self.kinopoisk_id = kinopoisk_id
        self.title_ru = title_ru
        self.title_en = title_en
        self.year = year
        self.poster = poster
        self.rating = rating
        self.description = description
        self.is_series = self._check_is_series(type)

    def _check_is_series(self, type):
        if type in ['TV_SERIES', 'MINI_SERIES']:
            return True
        return False


class KP_API:

    '''
    Класс отвечает за запросы и парсинг результатов с
    https://kinopoiskapiunofficial.tech/
    (неофициальный API Кинопоиск)
    '''

    def __init__(self, target, type):
        self.target = target
        self.type = type

    @staticmethod
    def send_request(target: str | int, type: str) -> list:
        match type:
            case 'keyword':
                response = requests.get(URLS[0] + target, headers=HEADERS)
            case 'seasons_info':
                response = requests.get(
                    URLS[1] + target + '/seasons', headers=HEADERS)
            case 'show_details':
                response = requests.get(URLS[1] + target, headers=HEADERS)
        return response.text

    @staticmethod
    def parse_response(target: str | int, type: str, format='local') -> KPResponse:
        result = []
        match type:
            case 'seasons_info':
                response = json.loads(KP_API.send_request(
                    f'{target}', type=type))

                if response['items']:
                    for season in response['items']:
                        episodes = []
                        for episode in season['episodes']:
                            episodes.append(
                                [item for item in episode.values()])
                        result.append(episodes)

            case 'keyword':
                response = json.loads(KP_API.send_request(
                    f'search-by-keyword?keyword={target}', type=type))
                if format == 'JSON':
                    return response['films']
                if response['films']:
                    for show in response['films']:
                        result.append(KPResponse(kinopoisk_id=show.get('filmId', ''),
                                                 title_ru=show.get(
                                                     'nameRu', ''),
                                                 title_en=show.get(
                                                     'nameEn', 'N/A'),
                                                 year=show.get('year', 'N/A'),
                                                 poster=show.get(
                                                     'posterUrl', ''),
                                                 rating=show.get(
                                                     'rating', 'N/A'),
                                                 description=show.get(
                                                     'description', 'N/A'),
                                                 type=show.get('type', 'N/A')))

            case 'show_details':
                response = json.loads(KP_API.send_request(
                    f'{target}', type=type))
                if response:
                    return KPResponse(kinopoisk_id=target,
                                      title_ru=response.get('nameRu', ''),
                                      title_en=response.get(
                                          'nameOriginal', 'N/A'),
                                      year=response.get('year', 'N/A'),
                                      poster=response.get('posterUrl', ''),
                                      rating=response.get(
                                          'ratingKinopoisk', 'N/A'),
                                      description=response.get(
                                          'description', 'N/A'),
                                      type=response.get('type', 'N/A'))

        return result
