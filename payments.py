
from mysql.connector import Error
from db import create_connection


def register_payment(session_id, payment_method):

    if payment_method not in ("cash", "card", "other"):
        print("Invalid payment method.")
        return None

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

        if amount is None or amount <= 0:
            print("Invalid parking fee.")
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

def get_unpaid_sessions():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            ps.session_id,
            ps.vehicle_id,
            v.plate_number,
            ps.fee,
            ps.status
        FROM parking_sessions ps
        LEFT JOIN payments p
            ON ps.session_id = p.session_id
        JOIN vehicles v
            ON ps.vehicle_id = v.vehicle_id
        WHERE p.payment_id IS NULL
        AND ps.status = 'completed'
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Error as error:
        print("Error getting unpaid sessions:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()

def get_payments():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            p.payment_id,
            p.session_id,
            v.plate_number,
            p.amount,
            p.payment_method,
            p.payment_time,
            p.payment_status
        FROM payments p
        JOIN parking_sessions ps
            ON p.session_id = ps.session_id
        JOIN vehicles v
            ON ps.vehicle_id = v.vehicle_id
        ORDER BY p.payment_id DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Error as error:
        print("Error getting payments:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
def search_payments(search_value):

    search_value = search_value.strip()

    if not search_value:
        return []

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor()

        if search_value.isdigit():

            query = """
            SELECT
                p.payment_id,
                p.session_id,
                v.plate_number,
                p.amount,
                p.payment_method,
                p.payment_time,
                p.payment_status
            FROM payments p
            JOIN parking_sessions ps
                ON p.session_id = ps.session_id
            JOIN vehicles v
                ON ps.vehicle_id = v.vehicle_id
            WHERE p.payment_id = %s
            """

        else:

            query = """
            SELECT
                p.payment_id,
                p.session_id,
                v.plate_number,
                p.amount,
                p.payment_method,
                p.payment_time,
                p.payment_status
            FROM payments p
            JOIN parking_sessions ps
                ON p.session_id = ps.session_id
            JOIN vehicles v
                ON ps.vehicle_id = v.vehicle_id
            WHERE v.plate_number = %s
            """

        cursor.execute(query, (search_value,))

        return cursor.fetchall()

    except Error as error:
        print("Error searching payments:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
def get_total_revenue():

    connection = create_connection()

    if connection is None:
        return 0

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT SUM(amount)
        FROM payments
        WHERE payment_status = 'paid'
        """

        cursor.execute(query)

        result = cursor.fetchone()

        total_revenue = result[0]

        if total_revenue is None:
            return 0

        return total_revenue

    except Error as error:
        print("Error getting total revenue:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()

def get_daily_revenue(report_date):

    connection = create_connection()

    if connection is None:
        return 0

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT SUM(amount)
        FROM payments
        WHERE payment_status = 'paid'
        AND DATE(payment_time) = %s
        """

        cursor.execute(query, (report_date,))

        result = cursor.fetchone()

        total_revenue = result[0]

        if total_revenue is None:
            return 0

        return total_revenue

    except Error as error:
        print("Error getting daily revenue:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()

def get_monthly_revenue(year, month):

    connection = create_connection()

    if connection is None:
        return 0

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT SUM(amount)
        FROM payments
        WHERE payment_status = 'paid'
        AND YEAR(payment_time) = %s
        AND MONTH(payment_time) = %s
        """

        cursor.execute(query, (year, month))

        result = cursor.fetchone()

        total_revenue = result[0]

        if total_revenue is None:
            return 0

        return total_revenue

    except Error as error:
        print("Error getting monthly revenue:", error)
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()