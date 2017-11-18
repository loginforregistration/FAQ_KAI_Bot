import sqlite3

class Db:
    """работа с базой данной происходяит только отсюда"""

    def search_by_word_with_like(database, table_name, column_where, word):
        db = sqlite3.connect(database)
        with db:
            cur = db.cursor()
            cur.execute("SELECT * "
                    "FROM " + table_name + " "
                                      "WHERE " + column_where + " LIKE '%" + word + "%'")

            return cur.fetchall()
