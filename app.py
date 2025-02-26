from flask import Flask
from controllers.SearchController import display_found_films
from models.Loger import Loger
from models.Searcher import Searcher


def run_web_app():
    app = Flask(__name__, template_folder='views/templates', static_folder='views/templates/css')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return display_found_films()

    app.run()

def run_console_app():
    while True:
        print("Выберите вариант поиска:")
        print("1. Поиск по жанру")
        print("2. Поиск по Наименованию")
        print("3. ТОП запросов поиска фильмов по популярности")
        print("4. ТОП запросов поиска фильмов по дате")
        print("Q. Выход")

        search_choice = input("Введите ваш выбор: ").strip().upper()
        searcher_in_db = Searcher()
        if search_choice == '1':
            search_by_genre(searcher_in_db)

        elif search_choice == '2':
            search_by_name(searcher_in_db)

        elif search_choice == '3':
            show_top_queries()

        elif search_choice == '4':
            show_recent_queries()

        elif search_choice == 'Q':
            break

def search_by_genre(searcher_in_db):
    genres = searcher_in_db.get_genres()
    print("Доступные жанры:")
    for index, genre in enumerate(genres, start=1):
        print(f"{index}. {genre}")

    genre_choice = input("Введите номер жанра: ").strip()
    try:
        genre_index = int(genre_choice) - 1
        if 0 <= genre_index < len(genres):
            selected_genre = genres[genre_index][0]
            films = searcher_in_db.get_films(None, selected_genre, None)
            print_films(films)
        else:
            print("Неверный выбор жанра.")
    except ValueError:
        print("Пожалуйста, введите корректный номер.")

def search_by_name(searcher_in_db):
    film_name = input("Введите наименование фильма: ").strip()
    films = searcher_in_db.get_films(film_name, None, None)
    print_films(films)

def show_top_queries():
    logger = Loger()
    top_queries = logger.get_top_queries()
    print("Топ-10 запросов по количеству:")
    for query, count in top_queries:
        print(f"{query}: {count}")

def show_recent_queries():
    logger = Loger()
    recent_queries = logger.get_recent_queries()
    print("Последние 10 запросов:")
    for query, date_query in recent_queries:
        print(f"{date_query}: {query}")

def print_films(films):
    count = 0
    for film in films:
        print(f"{count + 1}. {film[0]} - ({film[1]})")
        count += 1

        if count % 10 == 0 and count < len(films):
            choice = input("Нажмите N (Next) чтобы показать следующие 10 фильмов или Q (Quit) для выхода: ").strip().lower()
            if choice == 'q':
                break


def main():
    print("Выберите вариант запуска приложения:")
    print("1. Веб-режим")
    print("2. Консольный режим")
    print("Q. Выход")

    choice = input("Сделайте выбор (1, 2 или Q для выхода): ").strip().upper()

    if choice == '1':
        run_web_app()
    elif choice == '2':
        run_console_app()
    elif choice == 'Q':
        print("Выход из программы.")
    else:
        print("Неверный выбор. Пожалуйста, введите 1, 2 или Q.")
        main()

if __name__ == '__main__':
    main()
