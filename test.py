import psycopg2
from psycopg2 import OperationalError

def test_db_connection(dbname, user, password, host, port):
    try:
        # Attempt to establish a connection to the database
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        # Close the connection if successful
        conn.close()
        print("Database connection was successful!")
    except OperationalError as e:
        print(f"Failed to connect to the database: {e}")

# Replace these variables with your actual database connection details
dbname = 'portfolio'
user = 'postgres'
password = 'mamama00'
host = 'localhost'  # or 'localhost'
port = '5433'  # Ensure this is a string

test_db_connection(dbname, user, password, host, port)