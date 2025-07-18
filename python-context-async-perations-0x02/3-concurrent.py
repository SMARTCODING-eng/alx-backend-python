
import asyncio
import aiosqlite
import sqlite3



def set_up_database():
    with sqlite3.connect("user.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("""
                       CREATE TABLE users(
                           id INTEGER PRIMARY KEY,
                           name TEXT,
                           age INTEGER                       
                       )        
                    """)
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ('Alice', 30),
            ('Bob', 22),
            ('Charlie', 35),
            ('David', 45),
            ('Eve', 50)
        ])
        conn.commit()
    print("Database setup complete")



async def async_fetch_users():
    async with aiosqlite.connect("user.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        print("Fetched all users")
        return rows
    

async def async_fetch_older_users():
    async with aiosqlite.connect("user.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cursor.fetchall()
        print("Fetched users older than 40")
        return rows
    


async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("All Users:")
    for user in users:
        print(user)
    
    print("\nUsers Older Than 40:")
    for user in older_users:
        print(user)



if __name__ == "__main__":
    set_up_database()
    asyncio.run(fetch_concurrently())
