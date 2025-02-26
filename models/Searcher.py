from models.Connector import Connector
from models.Loger import Loger


class Searcher:

    def get_text_of_query(self, title=None, genre=None, year=None, actor=None):

        text = """SELECT film.title as title, film.description as description, 
        CONCAT(films_actor.first_name, ' ', films_actor.last_name) AS actor, film.release_year AS year 
        FROM film
        JOIN  (SELECT film_category.film_id, category.name as genre
                  FROM film_category
                  JOIN category ON film_category.category_id = category.category_id) AS films_genre
        ON film.film_id = films_genre.film_id  
      
        JOIN (SELECT film_actor.film_id as id, actor.first_name AS first_name, actor.last_name AS last_name FROM film_actor
        JOIN actor ON film_actor.actor_id = actor.actor_id) AS films_actor
        
        ON film.film_id =  films_actor.id 
        
        WHERE 1 = 1 """

        params = {}

        if genre is not None:
            text += " AND films_genre.genre = %(genre)s"
            params['genre'] = genre
        if title is not None:
            text += " AND film.title LIKE %(query)s"
            params['query'] = f"%{title}%"
            try:
                logger = Loger()
                logger.log_query(title)
            except Exception as e:
                print(f"Ошибка логирования запроса: {e}")

        if year is not None:
            if year.endswith('s'):
                start_year = int(year[:-1])
                end_year = start_year + 9
                text += f" AND film.release_year BETWEEN %(start_year)s AND %(end_year)s"
                params['start_year'] = start_year
                params['end_year'] = end_year
            elif year == 'old':
                text += " AND film.release_year < 1980"
            else:
                text += " AND film.release_year = %(year)s"
                params['year'] = int(year)

        if actor is not None:
            text += " AND CONCAT(films_actor.first_name, ' ', films_actor.last_name) = %(actor)s"
            params['actor'] = actor

        text += " ORDER BY film.title"

        return text, params


    def get_films(self, query=None, genre=None, year=None, actor=None):

        db_connector = Connector()
        connection, cursor = db_connector.get_db_connection('database')

        if connection:
            try:
                sql, params = self.get_text_of_query(query, genre, year, actor)
                cursor.execute(sql, params)
                result = cursor.fetchall()
                return result
            except Exception as e:
                print(f"Ошибка при получении фильмов: {e}")
                return None
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

