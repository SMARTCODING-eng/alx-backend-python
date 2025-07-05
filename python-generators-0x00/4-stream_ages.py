import mysql.connector
from mysql.connector import Error
#function that yield averae age of users one by one


def stream_user_ages():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Johnson1519',
            database='ALX_prodev'
        
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM users")
    except Error as e:
        print(f"Database error: {e}")
        yield None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def get_uaser_ages():
    total_age = 0.0
    count = 0
    for row in stream_user_ages():
        if row is None:
            continue
        age = row['age']
        if age is not None:
            total_age += age
            count += 1
            yield age

    if count > 0:
        average_age = total_age / count
        yield average_age
