import configparser

from flask import Flask
from controllers.SearchController import display_found_films
from models.Loger import Loger
from models.Searcher import Searcher
from models.TelegramBot import TelegramBot


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
        print("5. Поиск по жанру и году")
        print("6. Поиск по Наименованию и году")
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

        if search_choice == '5':
            search_by_genre(searcher_in_db, True)

        elif search_choice == '6':
            search_by_name(searcher_in_db, True)

        elif search_choice == 'Q':
            break

def search_by_genre(searcher_in_db, search_by_year = None):
    genres = searcher_in_db.get_genres()
    print("Доступные жанры:")
    for index, genre in enumerate(genres, start=1):
        print(f"{index}. {genre}")

    year = None
    genre_choice = input("Введите номер жанра: ").strip()

    try:
        genre_index = int(genre_choice) - 1
        if 0 <= genre_index < len(genres):
            selected_genre = genres[genre_index][0]

            if search_by_year:
                year = get_input_year()

            films = searcher_in_db.get_films(None, selected_genre, year)
            print_films(films)
        else:
            print("Неверный выбор жанра.")
    except ValueError:
        print("Пожалуйста, введите корректный номер.")

def search_by_name(searcher_in_db, search_by_year = None):
    year = None

    film_name = input("Введите наименование фильма: ").strip()
    if search_by_year:
        year = get_input_year()

    films = searcher_in_db.get_films(film_name, None, year)
    if not films:
        print(f'Фильмы c наименованием {film_name} не найдены.')
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
    print("Топ-10 запросов по дате:")
    for query, date_query in recent_queries:
        print(f"{date_query}: {query}")

def print_films(films):

    config = configparser.ConfigParser()
    config.read('settings.ini')
    quantity_of_films = int(config['app']['quantity_of_films'])

    if not quantity_of_films:
        quantity_of_films = 10

    if films:
        count = 0
        films_dict = {}
        for title, description, _, year in films:
            if title not in films_dict:
                films_dict[title] = (description, year)

        for title, (description, year) in films_dict.items():
            print(f"{title} - {description} - {year} год.")
            count += 1

            if count % quantity_of_films == 0 and count < len(films):
                choice = input(f"Нажмите N (Next) чтобы показать следующие {quantity_of_films}  фильмов или Q (Quit) для выхода: ").strip().lower()
                if choice == 'q':
                    break

def get_input_year():
    while True:
        year = input("Введите год: ").strip()
        if year.isdigit() and len(year) == 4:
            return int(year)
        else:
            print("Ошибка! Введите 4-значный год (например, 2025).")

def main():
    print("Выберите вариант запуска приложения:")
    print("1. Веб-режим")
    print("2. Консольный режим")
    print("3. Telegram-Bot")
    print("Q. Выход")

    offer_of_choice = "Введите 1, 2 ,3 или Q."

    choice = input(f"Сделайте выбор: ({offer_of_choice}): ").strip().upper()

    if choice == '1':
        run_web_app()
    elif choice == '2':
        run_console_app()
    elif choice == '3':
        bot = TelegramBot()
        bot.start_bot()
    elif choice == 'Q':
        print("Выход из программы.")
    else:
        print(f"Неверный выбор. {offer_of_choice}:")
        main()

if __name__ == '__main__':
    main()
