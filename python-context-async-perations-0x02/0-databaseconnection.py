import sqlite3

class DatabaseConnection:
    def __init__(self, database):

        self.database = database
        self.conn = None
        self.cursor = None


    def __enter__(self):
        self.conn = sqlite3.connect(self.database)
        self.cursor =self.conn.cursor()
        print("Database connection Opened.")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def query(self, sql_query):
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()



with DatabaseConnection("users.db") as db:
    db.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    db.cursor.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie')")
    db.conn.commit()

with DatabaseConnection("users.db") as db:
    result = db.query("SELECT * FROM users")
    for row in result:
        print(row)


        