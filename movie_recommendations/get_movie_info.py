import http.client
import json
from PIL import Image
import requests
from io import BytesIO

poster_url_constant = 'http://image.tmdb.org/t/p/w342/'


class MovieJsonKeys():
    name = 'title'
    overview = 'overview'
    vote_average = 'vote_average'
    poster_url = 'poster_path'
    genres = 'genres'
    homepage = 'homepage'
    popularity = 'popularity'
    release_date = 'release_date'
    revenue = 'revenue'
    runtime = 'runtime'


def get_movie_json(movie_id):
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    api_key = '9df6fc65ca74919ab7942a5792785196'
    payload = "{}"
    conn.request("GET", '/3/movie/' + str(movie_id) + '?language=en-US&api_key=' + api_key, payload)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    return json_data


if __name__ == "__main__":
    get_movie_json(movie_id=862)
