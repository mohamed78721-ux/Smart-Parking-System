
from mysql.connector import Error
from db import create_connection


def register_payment(session_id, payment_method):

    connection = create_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()

        # Step 1: Find the parking session
        query = """
        SELECT fee, status
        FROM parking_sessions
        WHERE session_id = %s
        """

        cursor.execute(query, (session_id,))
        session = cursor.fetchone()

        if session is None:
            print("Parking session not found.")
            return None

        # Step 2: Check if the session is completed
        if session[1] != "completed":
            print("Parking session is not completed.")
            return None

        # Step 3: Get the parking fee
        amount = session[0]

        if amount is None:
            print("Parking fee is not available.")
            return None

        # Step 4: Register the payment
        query = """
        INSERT INTO payments
        (session_id, amount, payment_method, payment_status)
        VALUES (%s, %s, %s, 'paid')
        """

        values = (session_id, amount, payment_method)

        cursor.execute(query, values)

        payment_id = cursor.lastrowid

        # Step 5: Save changes
        connection.commit()

        print("Payment registered successfully!")
        print("Payment ID:", payment_id)
        print("Amount:", amount, "SDG")
        print("Payment Method:", payment_method)

        return payment_id

    except Error as error:
        connection.rollback()
        print("Error registering payment:", error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
