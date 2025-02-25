from flask import request, render_template

from models.Loger import Loger
from models.Searcher import Searcher


def display_found_films():
    logger = Loger()
    searcher_in_db = Searcher()
    if request.method == 'POST':
        query = request.form.get('query', None)
        period = request.form.get('period', None)
        genre = request.form.get('genre', None)
        custom_year = request.form.get('customYear', None)

        if genre == "":
            genre = None
        if period == "":
            period = None
        if period == 'custom' and custom_year:
            year = int(custom_year)
        else:
            year = period
        films = searcher_in_db.get_films(query, genre, year)
        genres = searcher_in_db.get_genres()


        top_queries = logger.get_top_queries()
        recent_queries = logger.get_recent_queries()

        return render_template('index.html', genres=genres, films=films, top_queries=top_queries, recent_queries=recent_queries)

    genres = searcher_in_db.get_genres()
    top_queries = logger.get_top_queries()
    recent_queries = logger.get_recent_queries()
    return render_template('index.html', genres=genres, top_queries=top_queries, recent_queries=recent_queries)
