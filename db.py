import mysql.connector
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# ============================
# GET OWNER DETAILS
# ============================
def get_owner(vehicle_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT owner_name, email
        FROM vehicle_owners
        WHERE vehicle_number = %s
        """,
        (vehicle_no,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# ============================
# GET FINE AMOUNT
# ============================
def get_violation_fine(violation_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT fine
        FROM violation_types
        WHERE name = %s
        """,
        (violation_type,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else 500


# ============================
# SAVE FINE
# ============================
def save_fine(vehicle_no, email, fine, violation_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO traffic_fines
        (vehicle_number, email, fine, violation_type, paid)
        VALUES (%s, %s, %s, %s, 'N')
        """,
        (vehicle_no, email, fine, violation_type)
    )

    conn.commit()
    cursor.close()
    conn.close()


# ============================
# ADMIN ADD VEHICLE
# ============================
def add_vehicle(vehicle_no, owner_name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO vehicle_owners
        VALUES (%s, %s, %s, %s)
        """,
        (vehicle_no, owner_name, email, phone)
    )

    conn.commit()
    cursor.close()
    conn.close()
