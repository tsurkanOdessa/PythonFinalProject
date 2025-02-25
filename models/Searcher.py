
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


        if year is not None:
            if year.endswith('s'):
                start_year = int(year[:-1])
                end_year = start_year + 9
                text += " AND film.release_year BETWEEN %s AND %s"
                params.append(start_year)
                params.append(end_year)
            else:
                text += " AND film.release_year = %(year)s"
                params['year'] = int(year)

        return text, params