# add_vehicle.py
import sys
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection
from constants import COLORS, CAR_MAKES, CAR_MODELS
from PIL import Image
import subprocess

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

user_email = sys.argv[1] if len(sys.argv) > 1 else "user@example.com"

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

role_id = get_user_role(user_email)
if role_id is None or role_id not in (1, 2):
    messagebox.showerror("Error", "Unauthorized access")
    sys.exit(1)

# List of years from 1985 to 2025
YEARS = [str(year) for year in range(1985, 2026)]

# Initialize the main window
add_vehicle_window = ctk.CTk()
add_vehicle_window.title("Add Vehicle - QuickDrive Rentals")
add_vehicle_window.geometry("800x600")
add_vehicle_window.resizable(False, False)
add_vehicle_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(add_vehicle_window, fg_color=COLORS['color_1'], width=250, height=600)
sidebar_frame.pack_propagate(False)
sidebar_frame.place(x=0, y=0)

# Sidebar navigation options
nav_icons = {
    "home": ctk.CTkImage(light_image=Image.open("images/home_icon.png"), size=(50, 50)),
    "vehicle": ctk.CTkImage(light_image=Image.open("images/vehicle_icon.png"), size=(50, 50)),
    "customer": ctk.CTkImage(light_image=Image.open("images/customer_icon.png"), size=(50, 50)),
    "invoice": ctk.CTkImage(light_image=Image.open("images/invoice.png"), size=(50, 50)),
    "reports": ctk.CTkImage(light_image=Image.open("images/reports_icon.png"), size=(50, 50)),
    "logout": ctk.CTkImage(light_image=Image.open("images/logout_icon.png"), size=(50, 50))
}

# Home
dashboard_script = "staff_dashboard.py" if role_id == 2 else "admin_dashboard.py"
home_label = ctk.CTkLabel(sidebar_frame, text="Home", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['home'], compound="left", anchor="w", cursor="hand2")
home_label.pack(pady=10, padx=10, fill="x")
home_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), dashboard_script), user_email]) and add_vehicle_window.destroy())

# Vehicle Management
vehicle_label = ctk.CTkLabel(sidebar_frame, text="Vehicle Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['vehicle'], compound="left", anchor="w", width=200)
vehicle_label.pack(pady=10, padx=10, fill="x")

# Customer Management
customer_label = ctk.CTkLabel(sidebar_frame, text="Customer Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['customer'], compound="left", anchor="w", cursor="hand2")
customer_label.pack(pady=10, padx=10, fill="x")
customer_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_customer.py"), user_email]) and add_vehicle_window.destroy())

# Rental History
history_label = ctk.CTkLabel(sidebar_frame, text="Bookings/Invoices", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['invoice'], compound="left", anchor="w", cursor="hand2")
history_label.pack(pady=10, padx=10, fill="x")
history_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "rental_history.py"), user_email]) and add_vehicle_window.destroy())

# Reports
reports_label = ctk.CTkLabel(sidebar_frame, text="Reports", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['reports'], compound="left", anchor="w", cursor="hand2")
reports_label.pack(pady=10, padx=10, fill="x")
reports_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "reports.py"), user_email]) and add_vehicle_window.destroy())

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")]) and add_vehicle_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(add_vehicle_window, fg_color="white", width=600, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)

# Add Vehicle title
add_vehicle_title = ctk.CTkLabel(main_frame, text="Add Vehicle", font=("Arial", 24, "bold"), text_color="black")
add_vehicle_title.place(x=20, y=20)

# Form frame
form_frame = ctk.CTkScrollableFrame(main_frame, fg_color=COLORS['color_2'], width=350, height=400, scrollbar_button_color="gray", scrollbar_button_hover_color="darkgray")
form_frame.pack_propagate(False)
form_frame.place(x=80, y=100)

# Form fields
# Make
make_label = ctk.CTkLabel(form_frame, text="Make", font=("Arial", 16, "bold"), text_color="black")
make_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
make_var = tk.StringVar(value=CAR_MAKES[0])  # Default to first make
make_dropdown = ctk.CTkOptionMenu(form_frame, values=CAR_MAKES, variable=make_var, width=300, height=40, font=("Arial", 14))
make_dropdown.grid(row=1, column=0, padx=20, pady=5, sticky="w")

# Model
model_label = ctk.CTkLabel(form_frame, text="Model", font=("Arial", 16, "bold"), text_color="black")
model_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
model_var = tk.StringVar()
model_dropdown = ctk.CTkOptionMenu(form_frame, values=CAR_MODELS[CAR_MAKES[0]], variable=model_var, width=300, height=40, font=("Arial", 14))
model_dropdown.grid(row=3, column=0, padx=20, pady=5, sticky="w")

# Update model dropdown when make changes
def update_model_dropdown(*args):
    selected_make = make_var.get()
    models = CAR_MODELS.get(selected_make, [])
    model_dropdown.configure(values=models)
    model_var.set(models[0] if models else "")

make_var.trace("w", update_model_dropdown)

# Year
year_label = ctk.CTkLabel(form_frame, text="Year", font=("Arial", 16, "bold"), text_color="black")
year_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
year_var = tk.StringVar(value=YEARS[-1])  # Default to 2025
year_dropdown = ctk.CTkOptionMenu(form_frame, values=YEARS, variable=year_var, width=300, height=40, font=("Arial", 14))
year_dropdown.grid(row=5, column=0, padx=20, pady=5, sticky="w")

# License Plate
license_plate_label = ctk.CTkLabel(form_frame, text="License Plate", font=("Arial", 16, "bold"), text_color="black")
license_plate_label.grid(row=6, column=0, padx=20, pady=10, sticky="w")
license_plate_entry = ctk.CTkEntry(form_frame, width=300, height=40, border_color="black", border_width=1, font=("Arial", 14))
license_plate_entry.grid(row=7, column=0, padx=20, pady=5, sticky="w")

# Cost Per Day
cost_label = ctk.CTkLabel(form_frame, text="Cost Per Day ($)", font=("Arial", 16, "bold"), text_color="black")
cost_label.grid(row=8, column=0, padx=20, pady=10, sticky="w")
cost_entry = ctk.CTkEntry(form_frame, width=300, height=40, border_color="black", border_width=1, font=("Arial", 14))
cost_entry.grid(row=9, column=0, padx=20, pady=5, sticky="w")

# Add Vehicle button
add_button = ctk.CTkButton(form_frame, text="Add Vehicle", font=("Arial", 16, "bold"), fg_color=COLORS['color_1'], text_color="white", width=300, height=50, command=lambda: add_vehicle())
add_button.grid(row=10, column=0, padx=20, pady=20, sticky="w")

# Add vehicle function
def add_vehicle():
    make = make_var.get()
    model = model_var.get()
    year = year_var.get()
    license_plate = license_plate_entry.get().strip().upper()
    cost_per_day = cost_entry.get().strip()

    # Validate inputs
    if not all([make, model, year, license_plate]):
        messagebox.showerror("Error", "All fields are required")
        return

    # Validate make and model
    if make not in CAR_MAKES:
        messagebox.showerror("Error", "Invalid make selected")
        return
    if model not in CAR_MODELS.get(make, []):
        messagebox.showerror("Error", "Invalid model selected")
        return

    # Validate year
    try:
        year = int(year)
    except ValueError:
        messagebox.showerror("Error", "Year must be a valid number")
        return

    # Validate license plate
    if not (3 <= len(license_plate) <= 10 and license_plate.isalnum()):
        messagebox.showerror("Error", "License plate must be 3-10 alphanumeric characters")
        return

    # Validate cost per day
    try:
        cost_per_day = float(cost_per_day)
        if cost_per_day <= 0:
            messagebox.showerror("Error", "Cost per day must be a positive number")
            return
    except ValueError:
        messagebox.showerror("Error", "Cost per day must be a valid number")
        return

    # Check if license plate is unique
    conn = get_db_connection()
    if not conn:
        messagebox.showerror("Error", "Failed to connect to the database")
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM vehicles WHERE license_plate = %s", (license_plate,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "License plate already exists")
            return

        # Insert the vehicle into the database
        cursor.execute(
            "INSERT INTO vehicles (make, model, year, license_plate, cost_per_day, status) VALUES (%s, %s, %s, %s, %s, 'available')",
            (make, model, year, license_plate, cost_per_day)
        )
        conn.commit()
        messagebox.showinfo("Success", "Vehicle added successfully")
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "admin_dashboard.py"), user_email])
        add_vehicle_window.destroy()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to add vehicle: {e}")
    finally:
        cursor.close()
        conn.close()

add_vehicle_window.mainloop()