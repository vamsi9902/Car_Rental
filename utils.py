# utils.py
import mysql.connector
from PIL import Image, ImageTk
from config import Config


def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=Config["host"],
            user=Config["user"],
            password=Config["password"],
            database=Config["database"]
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def resize_image(size, image_path):
    try:
        image = Image.open(image_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None


def authenticate_user(email, password):
    conn = get_db_connection()
    if not conn:
        return (None, "Database connection failed")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            if user[6] == 'inactive':
                return (user, "Password Change Required")
            return (user, "Success")
        return (None, "Invalid email or password")
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return (None, f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def generate_email_address(first_name, last_name):
    #email generation for staff/admin
    return f"{first_name.lower()}.{last_name.lower()}@quickdrive.com"