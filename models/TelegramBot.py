import configparser
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ApplicationBuilder
import asyncio
from models.Connector import Connector
from models.Searcher import Searcher


class TelegramBot:

    def __init__(self):
        try:
            config = configparser.ConfigParser()
            config.read('settings.ini')
            self.key = config['telegram']['key']
            self.delete_message = config['telegram']['delete_message']
        except configparser.Error as e:
            self.key = None
            print(f"Ошибка! Отсутствует, либо пустой файл settings.ini: {e}")


    async def start(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text('Введите /byName и название фильма, что-бы найти фильм по наименованию ')
        await update.message.reply_text('Введите /byGenre и название жанра ,что-бы найти фильмы по жанру ')
        await update.message.reply_text('Введите /getGenres что-бы посмотреть жанры фильмов')
        await update.message.reply_text('Введите /cancel что-бы выйти')

    async def search_film_by_name(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            await update.message.reply_text('Пожалуйста, укажите название фильма.')
            return

        film_title = ' '.join(context.args)

        db_connector = Connector()
        connection, cursor = db_connector.get_db_connection('database')

        if connection:
            searcher_in_db = Searcher()
            films = searcher_in_db.get_films(film_title)
            if films:
                films_dict = {}
                for title, _, _, year in films:
                    if title not in films_dict:
                        films_dict[title] = year

                response = "\n".join([f"{title} - {year} год." for title, year in films_dict.items()])

                if update.message:
                    await update.message.reply_text(f'Найденные фильмы:\n{response}')
            else:
                await update.message.reply_text(f'Фильмы c наименованием {film_title} не найдены.')

    async def search_film_by_genre(self, update: Update, context: CallbackContext) -> None:

        if context.args:
            genre = ' '.join(context.args)
        else:
            await update.message.reply_text('Пожалуйста, укажите жанр фильма.')
            return



        db_connector = Connector()
        connection, cursor = db_connector.get_db_connection('database')

        if connection:
            searcher_in_db = Searcher()
            films = searcher_in_db.get_films(None, genre)
            if films:
                films_dict = {}
                for title, _, _, year in films:
                    if title not in films_dict:
                        films_dict[title] = year

                response = "\n".join([f"{title} - {year} год." for title, year in films_dict.items()])

                if update.message:
                    await update.message.reply_text(f'Найденные фильмы:\n{response}')
            else:
                await update.message.reply_text(f'Фильмы по жанру {genre} не найдены.')


    async def get_genres(self, update: Update, context: CallbackContext) -> None:

        db_connector = Connector()
        connection, cursor = db_connector.get_db_connection('database')

        if connection:
            searcher_in_db = Searcher()
            genres = searcher_in_db.get_genres()
            if genres:
                response = "\n".join(genre[0] for genre in genres)

                if update.message:
                    await update.message.reply_text(f'Найденные жанры:\n{response}')
                    await update.message.reply_text('Введите /byGenre и название жанра ,что-бы найти фильмы по жанру ')
            else:
                await update.message.reply_text(f'Жанры фильмов не найдены.')

    def get_name(update, context):
        update.message.reply_text("Введите название")
        return None

    async def cancel(self, update: Update, context: CallbackContext) -> None:
        if self.delete_message != 1:
            try:
                chat_id = update.message.chat_id
                message_id = update.message.message_id
                await update.message.delete()
                for i in range(15):
                    print('message_id ' + str(message_id) + str(message_id - i))
                    try:
                        await context.bot.delete_message(chat_id=chat_id, message_id=message_id - i)
                        await asyncio.sleep(0.2)
                    except Exception:
                        pass
            except Exception as e:
                print(f"Ошибка: {e}")

        context.user_data.clear()

    def start_bot(self):
        application = ApplicationBuilder().token(self.key).build()

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("byName", self.search_film_by_name))
        application.add_handler(CommandHandler("byGenre", self.search_film_by_genre))
        application.add_handler(CommandHandler("getGenres", self.get_genres))
        application.add_handler(CommandHandler("cancel", self.cancel))
        application.run_polling()