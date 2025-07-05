import mysql.connector
from mysql.connector import Error

def stream_users():

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Jonson1519',
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row

    except Error as e:
        print(f"database error: {e}")
        yield None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()



        