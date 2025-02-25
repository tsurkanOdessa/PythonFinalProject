import configparser

import mysql.connector as connector
from mysql.connector import Error


class Connector:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def get_db_connection(self,settings_name):
        try:
            config = configparser.ConfigParser()
            config.read('settings.ini')
        except configparser.Error as e:
            print(f"Ошибка! Отсутствует, либо пустой файл settings.ini: {e}")
            return self.connection, self.cursor

        host = config[settings_name]['host']
        user = config[settings_name]['user']
        password = config[settings_name]['password']
        database = config[settings_name]['database']
        charset = 'utf8mb4'

        try:
            conn = connector.connect(
                host=host, user=user, password=password, database=database, charset=charset
            )
            if conn.is_connected():
                self.connection = conn
                self.cursor = conn.cursor()
                return self.connection, self.cursor
        except Error as e:
            print(f"Ошибка: {e}")
            return self.connection, self.cursor

    def close_connect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()