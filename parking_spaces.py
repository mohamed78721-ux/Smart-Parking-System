from mysql.connector import Error
from db import create_connection

def add_parking_space(space_number, space_type, location=None):

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO parking_spaces
        (space_number, space_type, location)
        VALUES (%s, %s, %s)
        """

        values = (space_number, space_type, location)

        cursor.execute(query, values)

        connection.commit()

        print("Parking space added successfully!")
        print("Space ID:", cursor.lastrowid)

        return True

    except Error as error:
        connection.rollback()
        print("Error adding parking space:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()

#############################################################################
def view_parking_spaces():

    connection = create_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT space_id, space_number,
               space_type, status, location
        FROM parking_spaces
        """

        cursor.execute(query)

        spaces = cursor.fetchall()

        if not spaces:
            print("No parking spaces found.")
            return

        print("\n========== PARKING SPACES LIST ==========")

        for space in spaces:
            print("----------------------------------------")
            print("Space ID:", space[0])
            print("Space Number:", space[1])
            print("Space Type:", space[2])
            print("Status:", space[3])
            print("Location:", space[4])

        print("========================================")

    except Error as error:
        print("Error retrieving parking spaces:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
######################################################################################
def search_parking_space(space_number):

    connection = create_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT space_id, space_number,
               space_type, status, location
        FROM parking_spaces
        WHERE space_number = %s
        """

        values = (space_number,)

        cursor.execute(query, values)

        space = cursor.fetchone()

        if space is None:
            print("Parking space not found.")
            return

        print("\n========== PARKING SPACE FOUND ==========")
        print("Space ID:", space[0])
        print("Space Number:", space[1])
        print("Space Type:", space[2])
        print("Status:", space[3])
        print("Location:", space[4])
        print("=========================================")

    except Error as error:
        print("Error searching for parking space:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
##############################################################################
def update_parking_space(space_number, space_type, status, location):

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        # Check current parking space status

        cursor.execute("""
            SELECT status
            FROM parking_spaces
            WHERE space_number = %s
            FOR UPDATE
        """, (space_number,))

        space = cursor.fetchone()

        if space is None:
            return "not_found"

        current_status = space[0]

        # Prevent manual status changes while an active session exists

        if status != current_status:

            cursor.execute("""
                SELECT COUNT(*)
                FROM parking_sessions ps
                JOIN parking_spaces p
                    ON ps.space_id = p.space_id
                WHERE p.space_number = %s
                AND ps.status = 'active'
            """, (space_number,))

            active_sessions = cursor.fetchone()[0]

            if active_sessions > 0:
                connection.rollback()
                return "active_session"

        # Update parking space

        query = """
        UPDATE parking_spaces
        SET space_type = %s,
            status = %s,
            location = %s
        WHERE space_number = %s
        """

        values = (space_type, status, location, space_number)

        cursor.execute(query, values)

        connection.commit()

        return "success"

    except Error as error:

        connection.rollback()
        print("Error updating parking space:", error)

        return "error"

    finally:

        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
###############################################################################
def get_parking_spaces():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT space_id, space_number,
               space_type, status, location
        FROM parking_spaces
        """

        cursor.execute(query)

        spaces = cursor.fetchall()

        return spaces

    except Error as error:

        print("Error retrieving parking spaces:", error)
        return []

    finally:

        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
