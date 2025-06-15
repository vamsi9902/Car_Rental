# customer_dashboard.py
import sys
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection
from constants import COLORS
from PIL import Image
import subprocess
import sys

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

customer_email = sys.argv[1] if len(sys.argv) > 1 else "customer@example.com"

# Determine user role
def get_user_role(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role_id FROM users WHERE email = %s", (email,))
        role = cursor.fetchone()
        cursor.close()
        conn.close()
        return role[0] if role else None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch user role: {e}")
        return None

# Validate that the user is a customer (role_id = 3)
role_id = get_user_role(customer_email)
if role_id != 3:  # Only customers (role_id = 3) can access this page
    messagebox.showerror("Error", "Unauthorized access: Only customers can access the Customer Dashboard.")
    sys.exit(1)

customer_dashboard_window = ctk.CTk()
customer_dashboard_window.title("Customer Dashboard - QuickDrive Rentals")
customer_dashboard_window.geometry("800x600")
customer_dashboard_window.resizable(False, False)
customer_dashboard_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(customer_dashboard_window, fg_color=COLORS['color_1'], width=250, height=600)
sidebar_frame.pack_propagate(False)
sidebar_frame.place(x=0, y=0)

# Sidebar navigation options
nav_icons = {
    "home": ctk.CTkImage(light_image=Image.open("images/home_icon.png"), size=(50, 50)),
    "logout": ctk.CTkImage(light_image=Image.open("images/logout_icon.png"), size=(50, 50))
}

# Home
home_label = ctk.CTkLabel(sidebar_frame, text="Home", font=("Arial", 16, "bold"), text_color="black",
                          image=nav_icons['home'], compound="left", anchor="w", fg_color="#FFA500", width=200)
home_label.pack(pady=10, padx=10, fill="x")

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black",
                            image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>",
                  lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")]) and customer_dashboard_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(customer_dashboard_window, fg_color="white", width=600, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)


# Retrieve customer's name from the database
def get_customer_name(email):
    conn = get_db_connection()
    if not conn:
        return "Customer"

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT first_name, last_name FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return f"{user[0].capitalize()} {user[1].capitalize()}"
        return "Customer"
    except Exception as e:
        print(f"Error retrieving customer name: {e}")
        return "Customer"
    finally:
        cursor.close()
        conn.close()


customer_name = get_customer_name(customer_email)

# Welcome message
welcome_label = ctk.CTkLabel(main_frame, text=f"Welcome, {customer_name}!", font=("Arial", 24, "bold"),
                             text_color="black")
welcome_label.place(x=20, y=20)

# Action buttons
action_icons = {
    "view_booking": ctk.CTkImage(light_image=Image.open("images/view_booking_icon.png"), size=(50, 50)),
    "rental_history": ctk.CTkImage(light_image=Image.open("images/rental_history_icon.png"), size=(50, 50)),
    "book_vehicle": ctk.CTkImage(light_image=Image.open("images/book_vehicle_icon.png"), size=(50, 50))  # Increased icon size
}

# View Bookings button
view_bookings_button = ctk.CTkButton(main_frame, text="View Bookings", font=("Arial", 16, "bold"), fg_color="#E8E5DB",
                                     text_color="black", image=action_icons['view_booking'], compound="left",
                                     border_width=2, border_color="black", width=250, height=100,
                                     command=lambda: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "view_bookings.py"),
                                                                       customer_email]) and customer_dashboard_window.destroy())
view_bookings_button.place(x=100, y=100)

# Rental History button
rental_history_button = ctk.CTkButton(main_frame, text="Rental History", font=("Arial", 16, "bold"), fg_color="#E8E5DB",
                                      text_color="black", image=action_icons['rental_history'], compound="left",
                                      border_width=2, border_color="black", width=250, height=100,
                                      command=lambda: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "rental_history.py"),
                                                                        customer_email]) and customer_dashboard_window.destroy())
rental_history_button.place(x=100, y=250)

# Book a Vehicle button
book_vehicle_button = ctk.CTkButton(main_frame, text="Book a Vehicle", font=("Arial", 16, "bold"), fg_color="#E8E5DB",
                                    text_color="black", image=action_icons['book_vehicle'], compound="left",
                                    border_width=2, border_color="black", width=250, height=100,
                                    command=lambda: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "book_vehicle.py"),
                                                                      customer_email]) and customer_dashboard_window.destroy())
book_vehicle_button.place(x=100, y=400)

customer_dashboard_window.mainloop()