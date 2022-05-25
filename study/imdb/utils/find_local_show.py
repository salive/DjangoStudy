from ..models import Show


def find_local(query):
    local_shows = []
    try:
        shows = Show.objects.get(name=query.capitalize())
    except:
        return local_shows
    local_shows.append([shows.poster.url, shows.name])
    return local_shows
