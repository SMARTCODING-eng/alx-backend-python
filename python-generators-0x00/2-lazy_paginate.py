import mysql.connector
from mysql.connector import Error
def lazy_paginate(page_size, offset=0):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Johnson1519',
            databaase='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            cursor.execute("SELECT * FEROM user_data LIMIT")
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows
            offset += page_size


    except Error as e:
        print(f"Database error: {e}")
        yield None
        
