import sqlite3

class Db:
    """работа с базой данной происходяит только отсюда"""
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
    
    def search_by_word_with_like(self, table_name, column_where,word):
        with self.conn: # what if con is closed? #что произойдёт при закрытом соединении?
            self.cur.execute("SELECT * "
                    "FROM " + table_name + " "
                                      "WHERE " + column_where + " LIKE '%" + word + "%'")
        
            return self.cur.fetchall()

# if __name__=="__main__":
#     testDb=Db('db_001.db')
#     testlist =testDb.search_by_word_with_like('About_military', 'Question',"военк")
#     print (testlist)