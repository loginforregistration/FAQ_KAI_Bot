import sqlite3

class Db:
    """работа с базой данной происходяит только отсюда"""
    
    def search_by_word_with_like(self, database, table_name, column_where, word):
        self.db = sqlite3.connect(database)
        with self.db:
            cur = self.db.cursor()
            try:
                cur.execute("SELECT * "
                        "FROM " + table_name + " "
                                          "WHERE " + column_where + " LIKE '%" + word + "%'")
            except sqlite3.OperationalError:
                error = 1
            t=cur.fetchall()
            #self.db.close()
            return t
            
    
    def GetByColumnName(self,database, table_name, column_where, value):
        self.db = sqlite3.connect(database)
        with self.db:
            cur = self.db.cursor()
            cur.execute("SELECT * "
                    "FROM " + table_name + " "
                                        "WHERE " + column_where + " = '" + value + "'")
            t=cur.fetchall()
            #self.db.close()
            return t
    def Close(self):
        self.db.close()
