# create_tables.py
import mysql.connector
from constants import ROLES
from config import Config

def create_tables():
    try:
        conn = mysql.connector.connect(
            host=Config["host"],
            user=Config["user"],
            password=Config["password"],
            database=Config["database"]
        )
        cursor = conn.cursor()

        # Create Roles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                role_id INT PRIMARY KEY AUTO_INCREMENT,
                role_name VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        # Insert roles
        for role in ROLES:
            cursor.execute("INSERT IGNORE INTO roles (role_name) VALUES (%s)", (role,))

        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role_id INT NOT NULL,
                status ENUM('active', 'inactive') DEFAULT 'inactive',
                FOREIGN KEY (role_id) REFERENCES roles(role_id)
            )
        """)

        # Create Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                phone VARCHAR(20) NOT NULL,
                address1 VARCHAR(255) NOT NULL,
                address2 VARCHAR(255),
                city VARCHAR(100) NOT NULL,
                zipcode VARCHAR(10) NOT NULL,
                state VARCHAR(50) NOT NULL,
                driving_license_number VARCHAR(50),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Create Vehicles table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vehicles (
                        vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
                        make VARCHAR(50) NOT NULL,
                        model VARCHAR(50) NOT NULL,
                        year INT NOT NULL,
                        license_plate VARCHAR(20) NOT NULL UNIQUE,
                        cost_per_day DECIMAL(10, 2) NOT NULL,  -- Added cost per day
                        status ENUM('available', 'rented') DEFAULT 'available'
                    )
                """)

        # Create Rentals table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rentals (
                        rental_id INT PRIMARY KEY AUTO_INCREMENT,
                        customer_id INT NOT NULL,
                        vehicle_id INT NOT NULL,
                        start_date DATE NOT NULL,
                        end_date DATE NOT NULL,
                        total_cost DECIMAL(10, 2) NOT NULL,
                        status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
                    )
                """)


        conn.commit()
        print("Tables created successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()