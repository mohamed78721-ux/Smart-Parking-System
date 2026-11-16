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
