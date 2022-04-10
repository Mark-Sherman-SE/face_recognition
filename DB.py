import sqlite3

class DB:
    def __init__(self):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        try:
            create_table ='''CREATE TABLE sqlitedb (
                                            id INTEGER ,
                                            name TEXT ,
                                            login TEXT,
                                            PASSWORD TEXT);'''
            cursor.execute(create_table)
            list_users = [(1,"mrk","mash","123")]

            for id, nme, login, password in list_users:
                sqlite_insert_query = f"INSERT INTO sqlitedb (id,name,login,password)  VALUES  ({id},'{nme}', '{login}', '{password}');"
                cursor.execute(sqlite_insert_query)
            sqlite_connection.commit()

        except:
            pass

        self.cursor=cursor


