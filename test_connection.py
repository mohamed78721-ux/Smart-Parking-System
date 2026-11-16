
from db import create_connection

connection = create_connection()

if connection:
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES")

    tables = cursor.fetchall()

    print("\nDatabase Tables:")

    for table in tables:
        print(table[0])

    cursor.close()
    connection.close()
