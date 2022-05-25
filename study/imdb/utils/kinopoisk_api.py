import requests
import json


API_KEY = '22f7c6de-6224-4f2b-a718-ef79627c526a'
URL = 'https://kinopoiskapiunofficial.tech/api/v2.1/'
HEADERS = {
    'X-API-KEY': API_KEY
}


class KP_API:

    def __init__(self, target, type):
        self.target = target
        self.type = type

    @staticmethod
    def send_request(target: str) -> list:
        response = requests.get(URL + target, headers=HEADERS)
        return response.text

    @staticmethod
    def parse_response(keyword: str) -> list:
        shows = []
        res = json.loads(KP_API.send_request(
            f'films/search-by-keyword?keyword={keyword}'))
        if res['films']:
            for show in res['films']:
                shows.append([show.get('filmId', ''), show.get('nameRu', ''), show.get('year', ''),
                             show.get('description', ''), show.get('posterUrl', ''), show.get('rating', 'N/A')])
        return shows


KP_API.parse_response('Friends')
