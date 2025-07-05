import mysql.connector
from mysql.connector import Error
import csv


def connect_db():
    """connect to mysql server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Johnson1519',
        )
        print("Successfully connected to MYSQL server")
    except Error as e:
        print(f"Error connecting to MYSQL server: {e}")
    return connection

def create_database(connection):
    """create database ALX_prodev"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        connection.commit()


def connect_to_prodev():
    """connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Johnson1519',
            database='ALX_prodev'
        )
        print("Successfully connected to 'ALX_prodev' database")
        return connection
    except Error as e:
        print(f"Error connecting to 'ALX_prodev' database: {e}")
    return None

def create_table(connection):
    """create user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS user_data")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age INT NOT NULL
            )
        """)
        print("Table 'user_data' created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        connection.commit()

def insert_data(connection, data):
    """insert data from CSV file into user_data table"""
    try:
        cursor = connection.cursor()
        with open(data, 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)  # Skip header row
            for row in csv_data:
                if len(row) != 3:
                    print(f"Skipping invalid row: {row}")
                    continue
                name, email, age = row
                cursor.execute("INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.commit()
        