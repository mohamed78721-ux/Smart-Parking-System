import mysql.connector
from mysql.connector import Error

from db import create_connection


def add_vehicle(plate_number, vehicle_type, owner_name, owner_phone=None):

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO vehicles
        (plate_number, vehicle_type, owner_name, owner_phone)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            plate_number,
            vehicle_type,
            owner_name,
            owner_phone
        )

        cursor.execute(query, values)

        connection.commit()

        print("Vehicle added successfully!")
        print("Vehicle ID:", cursor.lastrowid)

        return True

    except Error as error:

        connection.rollback()

        print("Error adding vehicle:", error)

        return False

    finally:

        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()

def view_vehicles():

    connection = create_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor() #تنفيذ استعلام SQL لاسترجاع جميع المركبات من جدول المركبات

        query = """
        SELECT vehicle_id, plate_number,
               vehicle_type, owner_name, owner_phone
        FROM vehicles
        """

        cursor.execute(query)#تنفيذ الاستعلام واسترجاع النتائج

        vehicles = cursor.fetchall()#استرجاع جميع النتائج في قائمة

        if not vehicles:#التحقق مما إذا كانت القائمة فارغة، وإذا كانت كذلك، يتم طباعة رسالة تفيد بعدم وجود مركبات وإرجاع الدالة
            print("No vehicles found.")
            return

        print("\n========== VEHICLES LIST ==========")

        for vehicle in vehicles:
            print("----------------------------------")
            print("Vehicle ID:", vehicle[0])
            print("Plate Number:", vehicle[1])
            print("Vehicle Type:", vehicle[2])
            print("Owner Name:", vehicle[3])
            print("Owner Phone:", vehicle[4])

        print("==================================")

    except Error as error:#اذا حدث خطأ أثناء تنفيذ الاستعلام، يتم طباعة رسالة تفيد بوجود خطأ في استرجاع المركبات
        print("Error retrieving vehicles:", error)

    finally:#يستخدم البلوك finally لضمان إغلاق المؤشر والاتصال بقاعدة البيانات بعد الانتهاء من الاستعلام، سواء تم بنجاح أو حدث خطأ
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
#########################################################################################

def get_vehicles():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT vehicle_id, plate_number, vehicle_type,
               owner_name, owner_phone
        FROM vehicles
        """

        cursor.execute(query)

        vehicles = cursor.fetchall()

        return vehicles

    except Error as error:
        print("Error retrieving vehicles:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()

def delete_vehicle(vehicle_id):

    connection = create_connection()

    if connection is None:
        return "error"

    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether vehicle has parking sessions
        query = """
        SELECT COUNT(*)
        FROM parking_sessions
        WHERE vehicle_id = %s
        """

        cursor.execute(query, (vehicle_id,))
        result = cursor.fetchone()

        if result[0] > 0:
            print("Cannot delete vehicle: parking records exist.")
            return "has_sessions"

        # Delete vehicle
        query = """
        DELETE FROM vehicles
        WHERE vehicle_id = %s
        """

        cursor.execute(query, (vehicle_id,))

        if cursor.rowcount == 0:
            return "not_found"

        connection.commit()

        print("Vehicle deleted successfully!")

        return "success"

    except Error as error:

        connection.rollback()

        print("Error deleting vehicle:", error)

        return "error"

    finally:

        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()
