

class DatabaseConnection:
    def __init__(self ):
        self.connection = None
        self.cursor = None


    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value):
        self.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return False

    def query(self, query):
        with self:
            query = "SELECT * FROM users."
            self.cursor.execute(query)
            return self.cursor.fetchall()
        

