from mysql.connector import Error

from db import create_connection

import hashlib

def add_user(username, password, full_name, phone, role, status):
    connection = create_connection()
    
    if connection is None:
        return False
    
    cursor = None

    try:
        cursor = connection.cursor()

        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()
        query = """
        INSERT INTO users
        (username, password_hash, full_name, phone, role, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (username, password_hash, full_name, phone, role, status)

        cursor.execute(query, values)
        connection.commit()

        print("User added successfully!")
        print("User ID:", cursor.lastrowid)
        return True
    except Error as error:
        connection.rollback()
        print("Error adding user:", error)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()

#############################################################################
def view_users():

    connection = create_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT user_id, username, full_name, phone, role, status
        FROM users
        """

        cursor.execute(query)

        users = cursor.fetchall()

        if not users:
            print("No users found.")
            return

        print("\n========== USERS LIST ==========")

        for user in users:
            print("----------------------------------")
            print("User ID:", user[0])
            print("Username:", user[1])
            print("Full Name:", user[2])
            print("Phone:", user[3])
            print("Role:", user[4])
            print("Status:", user[5])

        print("==================================")

    except Error as error:
        print("Error retrieving users:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()

##############################################################################
def login_user(username, password):


    connection = create_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT user_id, username, password_hash, full_name, role
        FROM users
        WHERE username = %s AND status = 'active'
        """

        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user is None:
            return None

        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        if password_hash == user[2]:
            return user

        return None

    except Error as error:
        print("Login error:", error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()

