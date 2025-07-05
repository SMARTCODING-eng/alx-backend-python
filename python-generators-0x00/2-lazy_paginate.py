import mysql.connector
from mysql.connector import Error
def lazy_paginate(page_size):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Johnson1519',
            databaase='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        offset = 0
        while True:
            cursor.execute("SELECT * FEROM user_data LIMIT %s OFFSET %s, (page_size)")
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows
            offset += page_size


    except Error as e:
        print(f"Database error: {e}")
        yield None
        

