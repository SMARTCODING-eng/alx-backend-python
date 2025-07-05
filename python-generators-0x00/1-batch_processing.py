"""Write a function stream_users_in_batches(batch_size) that fetches rows in batches
"""

import mysql.connector
from mysql.connector import Error



def stream_users_in_bathes(batch_size):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Johnson1519',
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conection' in locals():
            connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_bathes(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user

# Example usage:
if __name__ == "__main__":
    batch_size = 10
    for user in batch_processing(batch_size):
        print(user)