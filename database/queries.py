INSERT_LANGUAGE = "INSERT INTO public.languages(language_code)VALUES(%s) ON CONFLICT(language_code) DO NOTHING;"
SELECT_ALL_LANGUAGES = "SELECT language_code, language_id FROM public.languages;"

INSERT_GENRE = "INSERT INTO public.genres (GENRE_NAME) VALUES(%s) ON CONFLICT(GENRE_NAME) DO NOTHING;"
SELECT_ALL_GENRES = "SELECT genre_name, genre_id FROM public.genres;"

INSERT_MOVIE = """
INSERT INTO public.movies
(movie_id, url, imdb_code, title, title_english, title_long, slug, release_year, rating, runtime, synopsis, 
trailer_code, mpa_rating, language_id)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (movie_id) do nothing;
"""

INSERT_MOVIE_GENRES = """
INSERT INTO public.movie_genre (movie_id, genre_id)VALUES(%s, %s) 
ON CONFLICT ON CONSTRAINT movie_genre_unique do nothing;
"""

INSERT_TORRENT = """
INSERT INTO public.torrents
(hash, movie_id, quality, torrent_type, seeds, peers, torrent_size_bytes, date_uploaded)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT(hash) DO NOTHING;
"""
