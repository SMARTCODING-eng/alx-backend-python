#!/usr/bin/python3
import seed
import csv
from mysql.connector import Error

def main():
    # Connect to MySQL server
    connection = seed.connect_db()
    if not connection:
        print("Failed to connect to MySQL server")
        return

    # Create database
    if not seed.create_database(connection):
        connection.close()
        return
    connection.close()
    print("Database creation successful")

    # Connect to ALX_prodev database
    connection = seed.connect_to_prodev()
    if not connection:
        print("Failed to connect to ALX_prodev database")
        return

    try:
        # Create table
        if not seed.create_table(connection):
            print("Failed to create table user_data")
            return

        # Insert data from CSV
        try:
            seed.insert_data(connection, 'user_data.csv')
        except FileNotFoundError:
            print("Error: CSV file 'user_data.csv' not found")
            return
        except Error as e:
            print(f"Error inserting data: {e}")
            return

    # Verify database and fetch sample data
        cursor = connection.cursor(dictionary=True)
        
        # Check if database exists
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev'")
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present")
        
        # Fetch sample data
        cursor.execute("SELECT * FROM user_data LIMIT 5")
        rows = cursor.fetchall()
        
        if rows:
            print("\nSample data from user_data table:")
            for row in rows:
                print(row)
        else:
            print("No data found in user_data table")

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        connection.close()

if __name__ == "__main__":
    main()