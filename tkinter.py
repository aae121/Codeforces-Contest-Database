import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="your_remote_host",
            user="your_username",
            password="your_password",
            database="your_database"
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
