from models.Connector import Connector
from models.Loger import Loger


class Searcher:

    def get_text_of_query(self, query=None, genre=None, year=None):
        text = """SELECT film.title as title, film.description as description, films_category.film_category as genre
                  FROM film
                  JOIN  (SELECT film_category.film_id, category.name AS film_category
                  FROM film_category
                  JOIN category ON film_category.category_id = category.category_id
                  WHERE 1 = 1 ) AS films_category
                  ON film.film_id = films_category.film_id
                  WHERE 2 = 2"""

        params = []

        if genre is not None:
            text = text.replace("1 = 1", "category.name = %s")
            params.append(genre)
        if query is not None:
            text = text.replace("2 = 2", "film.title LIKE %s")
            params.append("%" + query + "%")
            try:
                logger = Loger()
                logger.log_query(query)
            except Exception as e:
                print(f"Ошибка логирования запроса: {e}")

        if year is not None:
            if year.endswith('s'):
                start_year = int(year[:-1])
                end_year = start_year + 9
                text += " AND film.release_year BETWEEN %s AND %s"
                params.append(start_year)
                params.append(end_year)
            elif year == 'old':
                text += " AND film.release_year 1980"
            else:
                text += " AND film.release_year = %(year)s"
                params['year'] = int(year)

        return text, params


    def get_films(self, query=None, genre=None, year=None):
        db_connector = Connector()
        connection, cursor = db_connector.get_db_connection('database')

        if connection:
            try:
                with connection.cursor() as cursor:
                    sql, params = self.get_text_of_query(query, genre, year)
                    cursor.execute(sql, params)
                    return cursor.fetchall()
            except Exception as e:
                print(f"Ошибка при получении фильмов: {e}")
            finally:
                db_connector.close_connect()

    def get_genres(self):
        db_connector = Connector()
        connection, cursor = db_connector.get_db_connection('database')
        genres = []

        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT name FROM category")
                    genres = cursor.fetchall()
            except Exception as e:
                print(f"Ошибка при получении жанров: {e}")
            finally:
                db_connector.close_connect()
        return genres

