"""
create a class based context manager to handle opening and closing database connections automatically
Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods

Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.
"""
class DatabaseConnection:
    def __enter__(self):
        self.connection = "Database connection openeed"
        print(self.connection)
        return self
    
    def __exit__(self):
        print("Database connection closed")
        self.connection = None
        return False
    
    def query(self, sql):
        with sql == "SELECT * FROM users":
            return [
                {"id": 1, "name": "Ola mide"},
                {"id": 2, "name": "John Doe"}
            ]
        
with DatabaseConnection() as db:
    results = db.query("SELECT * FROM users")
    for row in results:
        print(row)  