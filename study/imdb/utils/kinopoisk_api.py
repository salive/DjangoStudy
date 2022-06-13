from urllib import response
import requests
import json


API_KEY = '22f7c6de-6224-4f2b-a718-ef79627c526a'
URLS = ['https://kinopoiskapiunofficial.tech/api/v2.1/films/',
        'https://kinopoiskapiunofficial.tech/api/v2.2/films/']
HEADERS = {
    'X-API-KEY': API_KEY
}


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
    def parse_response(target: str | int, type: str) -> list:
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
                if response['films']:
                    for show in response['films']:
                        result.append([show.get('filmId', ''), show.get('type', ''), show.get('nameRu', ''), show.get('year', ''),
                                       show.get('description', ''), show.get('posterUrl', ''), show.get('rating', 'N/A')])

            case 'show_details':
                response = json.loads(KP_API.send_request(
                    f'{target}', type=type))
                if response:
                    return (response['posterUrl'], response['nameRu'], response['nameOriginal'],
                            response['ratingKinopoisk'], response['year'], response['description'], response['type'])

        return result
