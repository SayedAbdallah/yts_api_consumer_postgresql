from typing import List, Dict, Tuple
import configparser
from database import yts_database


def read_config() -> Dict:
    config = configparser.ConfigParser()
    config.read('yts.ini')
    return dict(config['DEFAULT'].items())


def _insert_languages(cur, languages: List[Tuple]) -> None:
    yts_database.insert_languages(cur=cur, languages=languages)


def _insert_genres(cur, genres: List[Tuple]) -> None:
    yts_database.insert_genres(cur=cur, genres=genres)


def _insert_movie_genres(cur, movie_genres: List[Tuple]):
    yts_database.insert_movie_genres(cur=cur, movie_genres=movie_genres)


def _insert_movies(cur, movies: List[Tuple]) -> None:
    yts_database.insert_movies(cur=cur, movies=movies)


def _insert_torrents(cur, torrents: List[Tuple]) -> None:
    yts_database.insert_torrents(cur=cur, torrents=torrents)


def _format_movie(movie: Dict, db_languages: Dict) -> Tuple:
    movie_id = movie.get('id')
    url = movie.get('url')
    imdb_code = movie.get('imdb_code')
    title = movie.get('title')
    title_english = movie.get('title_english')
    title_long = movie.get('title_long')
    slug = movie.get('slug')
    release_year = movie.get('year')
    rating = movie.get('rating')
    runtime = movie.get('runtime')
    synopsis = movie.get('synopsis')
    trailer_code = movie.get('yt_trailer_code')
    language_id = db_languages.get(movie.get('language'))
    mpa_rating = movie.get('mpa_rating')

    return (movie_id, url, imdb_code, title, title_english, title_long, slug, release_year,
            rating, runtime, synopsis, trailer_code, mpa_rating, language_id)


def _format_torrent(torrents: List[Dict], movie_id: int) -> List[Tuple]:
    torrents_to_return = []
    for torrent in torrents:
        t = (torrent['hash'],
             movie_id,
             torrent['quality'],
             torrent['type'],
             torrent['seeds'],
             torrent['peers'],
             torrent['size_bytes'],
             torrent['date_uploaded']
             )
        torrents_to_return.append(t)

    return torrents_to_return


def process_movies(movies: List[Dict]) -> None:
    """
    Handle an list of movies dictionaries and insert data into database

    :param movies: json array represent each movie with all data
    :return: None
    """
    # torrents = [t for movie in movies for t in movie.get('torrents', [])]
    con = yts_database.connect(read_config())
    cur = con.cursor()

    db_languages = yts_database.select_all_languages(cur=cur)
    db_genres = yts_database.select_all_genres(cur=cur)

    languages = list({(movie['language'],) for movie in movies if movie['language'] not in db_languages.keys()})
    genres = list({(g,) for movie in movies for g in movie.get('genres', []) if g not in db_genres.keys()})

    if len(languages) > 0:
        _insert_languages(cur=cur, languages=languages)
        con.commit()
        db_languages = yts_database.select_all_languages(cur=cur)

    if len(genres) > 0:
        _insert_genres(cur=cur, genres=genres)
        con.commit()
        db_genres = yts_database.select_all_genres(cur=cur)

    movies_to_insert = []
    movie_genres_to_insert = []
    torrents_to_insert = []

    for movie in movies:
        m = _format_movie(movie=movie, db_languages=db_languages)
        movies_to_insert.append(m)

        genres = [(movie['id'], db_genres[g]) for g in movie.get('genres', [])]
        movie_genres_to_insert.extend(genres)

        torrents = _format_torrent(torrents=movie.get('torrents', []), movie_id=movie['id'])
        torrents_to_insert.extend(torrents)

    _insert_movies(cur=cur, movies=movies_to_insert)
    _insert_movie_genres(cur=cur, movie_genres=movie_genres_to_insert)
    _insert_torrents(cur=cur, torrents=torrents_to_insert)

    con.commit()
    cur.close()
    con.close()
