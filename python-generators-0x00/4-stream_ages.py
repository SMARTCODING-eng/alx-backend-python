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
        cursor.execute("SELECT age FROM user  data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row['age']


    except Error as e:
        print(f"Database error: {e}")
        yield None

