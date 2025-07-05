#!/usr/bin/python3
import seed
# This script connects to a database, creates a schema, and inserts data from a CSV file.


seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        if seed.create_table(connection):
            seed.insert_data(connection, 'user_data.csv')
        else:
            print("Failed to create table user_data")
        cursor = connection.cursor()
        # Check if the database ALX_prodev exists
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print("Simple data:", rows)
        cursor.close()
    else:
        print("Failed to connect to ALX_prodev database")
        connection.close()

