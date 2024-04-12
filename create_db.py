import sqlite3

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

# Create the table if it does not exist
def create_table(conn):
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

# Main function
def main():
    database = "users.db"
    
    # Create a database connection
    conn = create_connection(database)
    
    if conn is not None:
        # Create users table
        create_table(conn)
        conn.close()
        print("Database created successfully.")
    else:
        print("Error! Cannot create the database connection.")

if name == 'main':
    main()