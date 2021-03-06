import psycopg2
import database.queries as q
from typing import Dict, List, Tuple


def connect(connection_info: Dict):
    con = psycopg2.connect(host=connection_info['host'], port=connection_info['port'],
                           database=connection_info['database'], user=connection_info['user'],
                           password=connection_info['password'])
    return con


def insert_languages(cur, languages: List[Tuple]) -> None:
    cur.executemany(q.INSERT_LANGUAGE, languages)


def select_all_languages(cur) -> Dict[str, int]:
    cur.execute(q.SELECT_ALL_LANGUAGES)
    return dict(cur.fetchall())


def insert_genres(cur, genres: List[Tuple]) -> None:
    cur.executemany(q.INSERT_GENRE, genres)


def select_all_genres(cur) -> Dict[str, int]:
    cur.execute(q.SELECT_ALL_GENRES)
    return dict(cur.fetchall())


def insert_movie_genres(cur, movie_genres: List[Tuple]):
    cur.executemany(q.INSERT_MOVIE_GENRES, movie_genres)


def insert_movies(cur, movies: List[Tuple]):
    cur.executemany(q.INSERT_MOVIE, movies)


def insert_torrents(cur, torrents: List[Tuple]):
    cur.executemany(q.INSERT_TORRENT, torrents)
