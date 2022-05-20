import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}


def parse(target):
    print(target)
    response = requests.get(target, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find('div', class_='rating').find_all('a')
    result = []
    for m in movies:
        href = m['href']
        image = m.find('img')['src']
        title = str(m.find('strong').get_text())
        if image != '/images/empty/posters/400x450.png':
            result.append([image, title, href])
    return result
