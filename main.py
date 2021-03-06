from Utils import process_movies
from YTS_Consumer.YTSConsumer import YTSConsumer

BASE_URL = "https://yts.mx/api/v2/list_movies.json?limit={}&page={}"
LIMIT = 50


def start_consuming() -> None:
    page = 1
    while True:
        try:
            print(f'Start to scrap page {page}')
            url = BASE_URL.format(LIMIT, page)
            movies = YTSConsumer.consume(url=url)
            process_movies(movies=movies)
            page += 1

        except KeyError:
            print('Finish Scrapping all Movies')
            break


if __name__ == '__main__':
    start_consuming()
