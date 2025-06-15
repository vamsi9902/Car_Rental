#signup.py
import sys
import os
import customtkinter as ctk
from tkinter import messagebox
import re
from utils import get_db_connection, resize_image
from constants import COLORS, ROLES, US_STATES
import subprocess

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

# Initialize the main window
signup_window = ctk.CTk()
signup_window.title("Sign Up - QuickDrive Rentals")
signup_window.geometry("800x600")
signup_window.resizable(False, False)
signup_window.configure(fg_color=COLORS['color_1'])

# Left frame for signup form
left_frame = ctk.CTkScrollableFrame(signup_window, fg_color=COLORS['color_2'], width=400, height=400, scrollbar_button_color="gray", scrollbar_button_hover_color="darkgray")
left_frame.pack_propagate(False)
left_frame.place(x=50, y=100)

# Logo at the top-left
logo_image = resize_image((100, 50), 'images/loginLogo.jpg')
logo_label = ctk.CTkLabel(signup_window, text="", image=logo_image)
logo_label.place(x=20, y=20)

# Logo Title
logotitle_label = ctk.CTkLabel(signup_window, text="QuickDrive Rentals", font=("Aclonica", 16, "bold"), text_color="white")
logotitle_label.place(x=90, y=20)

# Signup form title
signup_title = ctk.CTkLabel(left_frame, text="Sign Up", font=("Abril Fatface", 18, "bold"), text_color="black")
signup_title.grid(row=0, column=0, columnspan=1, pady=10, padx=170, sticky="w")

# Email validation regex
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Form fields
email_label = ctk.CTkLabel(left_frame, text="Email", font=("Abril Fatface", 12, "bold"), text_color="black")
email_label.grid(row=1, column=0, padx=50, pady=5, sticky="w")
email_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="abc@gmail.com")
email_entry.grid(row=2, column=0, padx=50, pady=5, sticky="w")

first_name_label = ctk.CTkLabel(left_frame, text="First Name", font=("Abril Fatface", 12, "bold"), text_color="black")
first_name_label.grid(row=3, column=0, padx=50, pady=5, sticky="w")
first_name_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="John")
first_name_entry.grid(row=4, column=0, padx=50, pady=5, sticky="w")

last_name_label = ctk.CTkLabel(left_frame, text="Last Name", font=("Abril Fatface", 12, "bold"), text_color="black")
last_name_label.grid(row=5, column=0, padx=50, pady=5, sticky="w")
last_name_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="Doe")
last_name_entry.grid(row=6, column=0, padx=50, pady=5, sticky="w")

phone_label = ctk.CTkLabel(left_frame, text="Phone", font=("Abril Fatface", 12, "bold"), text_color="black")
phone_label.grid(row=7, column=0, padx=50, pady=5, sticky="w")
phone_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="999-999-9999")
phone_entry.grid(row=8, column=0, padx=50, pady=5, sticky="w")

address1_label = ctk.CTkLabel(left_frame, text="Address 1", font=("Abril Fatface", 12, "bold"), text_color="black")
address1_label.grid(row=9, column=0, padx=50, pady=5, sticky="w")
address1_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="Street Address")
address1_entry.grid(row=10, column=0, padx=50, pady=5, sticky="w")

address2_label = ctk.CTkLabel(left_frame, text="Address 2 (Optional)", font=("Abril Fatface", 12, "bold"), text_color="black")
address2_label.grid(row=11, column=0, padx=50, pady=5, sticky="w")
address2_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="App/Suite")
address2_entry.grid(row=12, column=0, padx=50, pady=5, sticky="w")

city_label = ctk.CTkLabel(left_frame, text="City", font=("Abril Fatface", 12, "bold"), text_color="black")
city_label.grid(row=13, column=0, padx=50, pady=5, sticky="w")
city_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="City")
city_entry.grid(row=14, column=0, padx=50, pady=5, sticky="w")

zipcode_label = ctk.CTkLabel(left_frame, text="Zipcode", font=("Abril Fatface", 12, "bold"), text_color="black")
zipcode_label.grid(row=15, column=0, padx=50, pady=5, sticky="w")
zipcode_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="Zip")
zipcode_entry.grid(row=16, column=0, padx=50, pady=5, sticky="w")

# State dropdown
state_label = ctk.CTkLabel(left_frame, text="State", font=("Abril Fatface", 12, "bold"), text_color="black")
state_label.grid(row=17, column=0, padx=50, pady=5, sticky="w")
state_dropdown = ctk.CTkOptionMenu(left_frame, width=300, values=US_STATES)
state_dropdown.grid(row=18, column=0, padx=50, pady=5, sticky="w")

# Signup button inside the left frame
signup_button = ctk.CTkButton(left_frame, text="Sign Up", width=300, height=40, fg_color="#1B5671", text_color="white", command=lambda: create_account())
signup_button.grid(row=21, column=0, padx=50, pady=(30,0), sticky="w")

# Back to login link inside the left frame
back_label = ctk.CTkLabel(left_frame, text="Already have an account?", font=("Arial", 10), text_color="black")
back_label.grid(row=22, column=0, padx=120, pady=0, sticky="w")
back_link = ctk.CTkLabel(left_frame, text="Login", font=("Arial", 10, "bold"), text_color="black", cursor="hand2")
back_link.grid(row=22, column=0, padx=235, pady=0, sticky="w")
back_link.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")]) and signup_window.destroy())

# Right side Car Banner
car_image = resize_image((600, 1200), 'images/loginBanner.jpg')
car_label = ctk.CTkLabel(signup_window, text="", image=car_image)
car_label.place(x=500, y=0)

# Validation and account creation
def validate_email(email):
    return re.match(EMAIL_PATTERN, email) is not None

def check_email_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

def validate_zipcode(zipcode):
    # zipcode validation
    return re.match(r'^\d{5}(-\d{4})?$', zipcode) is not None

def create_account():
    email = email_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone = phone_entry.get()
    address1 = address1_entry.get()
    address2 = address2_entry.get()
    city = city_entry.get()
    zipcode = zipcode_entry.get()
    state = state_dropdown.get()

    # Required fields (address2 is optional)
    if not all([email, first_name, last_name, phone, address1, city, zipcode, state]):
        messagebox.showerror("Error", "All required fields must be filled")
        return

    # Validate email format
    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return

    # Check if email already exists
    if check_email_exists(email):
        messagebox.showerror("Error", "Email already in use")
        return

    # Validate zipcode
    if not validate_zipcode(zipcode):
        messagebox.showerror("Error", "Invalid zipcode format (e.g., 12345 or 12345-6789)")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert into Users table
        cursor.execute("INSERT INTO users (first_name, last_name, email, password, role_id, status) VALUES (%s, %s, %s, %s, %s, %s)",
                       (first_name.lower(), last_name.lower(), email, 'password', ROLES.index('customer') + 1, 'inactive'))
        user_id = cursor.lastrowid
        # Insert into Customers table
        cursor.execute("INSERT INTO customers (user_id, phone, address1, address2, city, zipcode, state) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (user_id, phone, address1, address2, city, zipcode, state))
        conn.commit()
        messagebox.showinfo("Success", f"Account created successfully with email {email}. Please log in and change your password.")
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")])
        signup_window.destroy()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to create account: {e}")
    finally:
        cursor.close()
        conn.close()

signup_window.mainloop()