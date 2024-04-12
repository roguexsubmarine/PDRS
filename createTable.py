import sqlite3

def get_db_connection():
    conn = sqlite3.connect('user.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the table if it does not exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
print("creating table...")
create_table()
print("...done")