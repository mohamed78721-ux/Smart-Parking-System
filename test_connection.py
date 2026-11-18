
from db import create_connection

def main():
    connection = create_connection()

    if connection:
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            print("\nDatabase Tables:")
            for table in tables:
                print(table[0])
        finally:
            if cursor is not None:
                cursor.close()
            if connection.is_connected():
                connection.close()


if __name__ == "__main__":
    main()
