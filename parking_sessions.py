from mysql.connector import Error
from db import create_connection


def register_vehicle_entry(vehicle_id, space_id, user_id=None):

    connection = create_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()

        # Step 1: Check if the vehicle exists

        query = """
        SELECT vehicle_id
        FROM vehicles
        WHERE vehicle_id = %s
        """

        cursor.execute(query, (vehicle_id,))

        vehicle = cursor.fetchone()

        if vehicle is None:
            print("Vehicle not found.")
            return None

        # Step 2: Check parking space availability

        query = """
        SELECT status
        FROM parking_spaces
        WHERE space_id = %s
        FOR UPDATE
        """

        cursor.execute(query, (space_id,))

        space = cursor.fetchone()

        if space is None:
            print("Parking space not found.")
            return None

        if space[0] != "available":
            print("Parking space is not available.")
            return None

        # Step 3: Check active session for this vehicle

        query = """
        SELECT session_id
        FROM parking_sessions
        WHERE vehicle_id = %s
        AND status = 'active'
        """

        cursor.execute(query, (vehicle_id,))

        active_session = cursor.fetchone()

        if active_session is not None:
            print("Vehicle already has an active parking session.")
            return None

        # Step 4: Create a new parking session

        query = """
        INSERT INTO parking_sessions
        (vehicle_id, space_id, user_id, status)
        VALUES (%s, %s, %s, 'active')
        """

        values = (vehicle_id, space_id, user_id)

        cursor.execute(query, values)

        session_id = cursor.lastrowid

        # Step 5: Update parking space status

        query = """
        UPDATE parking_spaces
        SET status = 'occupied'
        WHERE space_id = %s
        """

        cursor.execute(query, (space_id,))

        # Step 6: Save all changes

        connection.commit()

        print("Vehicle entry registered successfully!")
        print("Session ID:", session_id)

        return session_id

    except Error as error:
        connection.rollback()
        print("Error registering vehicle entry:", error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
#############################################################################

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


def register_vehicle_exit(vehicle_id):

    connection = create_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()

        # Step 1: Find active parking session

        query = """
        SELECT session_id, space_id, entry_time
        FROM parking_sessions
        WHERE vehicle_id = %s
        AND status = 'active'
        """

        cursor.execute(query, (vehicle_id,))
        session = cursor.fetchone()

        if session is None:
            print("No active parking session found.")
            return None

        session_id = session[0]
        space_id = session[1]
        entry_time = session[2]

        # Step 2: Calculate parking duration

        exit_time = datetime.now()

        duration = exit_time - entry_time
        duration_minutes = max(0, int(duration.total_seconds() // 60))

        # Step 3: Calculate parking fee
        # 1000 SDG per hour

        fee = (
            Decimal(duration_minutes) * Decimal(1000) / Decimal(60)
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Step 4: Update parking session

        query = """
        UPDATE parking_sessions
        SET exit_time = %s,
            duration_minutes = %s,
            fee = %s,
            status = 'completed'
        WHERE session_id = %s
        """

        cursor.execute(
            query,
            (exit_time, duration_minutes, fee, session_id)
        )

        # Step 5: Make parking space available again

        query = """
        UPDATE parking_spaces
        SET status = 'available'
        WHERE space_id = %s
        """

        cursor.execute(query, (space_id,))

        # Step 6: Save changes

        connection.commit()

        print("Vehicle exit registered successfully!")
        print("Duration:", duration_minutes, "minutes")
        print("Parking fee:", fee, "SDG")

        return fee

    except Error as error:
        connection.rollback()
        print("Error registering vehicle exit:", error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
