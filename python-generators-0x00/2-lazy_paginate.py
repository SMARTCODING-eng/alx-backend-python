import mysql.connector
from mysql.connector import Error
def paginate_users(page_size, offset):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Johnson1519',
            databaase='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        
        
       
        cursor.execute(
            "SELECT * FEROM user_data LIMIT"
            
        )
        return cursor.fetchall()
    
            
    except Error as e:
        print(f"Database error: {e}")
        yield None
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals:
            connection.close()





def paginate_user(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size     
            
    
        
