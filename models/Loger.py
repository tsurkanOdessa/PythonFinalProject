import sqlite3
from datetime import datetime

class Loger:
    def __init__(self, db_name='user_queries.db'):
        self.db_name = db_name
        self.create_table()

    def create_table(self):

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_query (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    date_query TIMESTAMP NOT NULL
                )
            ''')
            conn.commit()

    def log_query(self, user_query):
        if len(user_query) == 0:
            return None
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_query (query, date_query)
                VALUES (?, ?)
            ''', (user_query, datetime.now()))
            conn.commit()

    def get_top_queries(self, limit=10):

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT query, COUNT(*) as count
                FROM user_query
                GROUP BY query
                ORDER BY count DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def get_recent_queries(self, limit=10):

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT query, strftime('%Y-%m-%d %H:%M:%S', date_query) as date_query
                FROM user_query
                ORDER BY date_query DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def clear_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_query')
            conn.commit()