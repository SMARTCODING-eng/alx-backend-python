import sqlite3

class ExecuteQuery:
    def __init__(self, query, params, database="users.db"):
        self.query = query
        self.params = params
        self.database = database
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        print("Database connection opened")
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result
    

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

with sqlite3.connect("users.db") as conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
        ('Alice', 30),
        ('Bob', 22),
        ('Charlie', 35)
    ])
    conn.commit()
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params, "users.db") as result:
    print("Quering result")
    for row in result:
        print(row)


