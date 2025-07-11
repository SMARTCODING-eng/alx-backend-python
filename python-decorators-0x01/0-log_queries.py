import sqlite3
import functools
from datetime import datetime


def log_queries():
    """
    Decorator to log SQL queries executed on a SQLite database.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = args[0] if args else kwargs.get('query', '')
            start_time = datetime.now()
            print(f"Executing query: {query}")
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = end_time - start_time
            print(f"Query executed in: {duration}")
            return result
        return wrapper
    return decorator

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results



users = fetch_all_users(query="SELECT * FROM users")