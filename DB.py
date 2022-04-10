import sqlite3


class DB:
    def __init__(self):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        try:
            create_table = '''CREATE TABLE sqlitedb (
                                            id INTEGER ,
                                            name TEXT ,
                                            login TEXT,
                                            PASSWORD TEXT);'''
            cursor.execute(create_table)
            list_users = [[0, "Aditya_Seal", "adse", 1234],
                          [1, "Agata_Passent", "agpa", 1234],
                          [2, "Ana_Rosa_Quintana", "anro", 1234],
                          [3, "Andrea_Anders", "anan", 1234],
                          [4, "Caio_Riberio", "cari", 1234],
                          [5, "Carlo_Conti", "caco", 1234],
                          [6, "Diana_Bolocco", "dibo", 1234],
                          [7, "Eve_Plumb", "evpl", 1234],
                          [8, "Felipe_Claderin", "fecl", 1234],
                          [9, "Gregg_Popovich", "grpo", 1234],
                          [10, "Mari_Dorin_Habert", "mado", 1234],
                          [11, "Mark_Sherman", "mash", 123456789],
                        ]

            for id, nme, login, password in list_users:
                sqlite_insert_query = f"INSERT INTO sqlitedb (id,name,login,password)  VALUES  ({id},'{nme}', '{login}', '{password}');"
                cursor.execute(sqlite_insert_query)
            sqlite_connection.commit()

        except:
            pass

        self.cursor = cursor
