# manage_vehicles.py
import sys
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection, resize_image
from constants import COLORS
import subprocess
from PIL import Image
import sys
import re

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

# Get the user's email from command-line arguments
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
if role_id is None or role_id not in (1, 2):  # Only admin (1) and staff (2) can access this
    messagebox.showerror("Error", "Unauthorized access")
    sys.exit(1)

# Initialize the main window
manage_vehicles_window = ctk.CTk()
manage_vehicles_window.title("Manage Vehicles - QuickDrive Rentals")
manage_vehicles_window.geometry("1000x600")
manage_vehicles_window.resizable(False, False)
manage_vehicles_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(manage_vehicles_window, fg_color=COLORS['color_1'], width=250, height=600)
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
home_label = ctk.CTkLabel(sidebar_frame, text="Home", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['home'], compound="left", anchor="w", cursor="hand2")
home_label.pack(pady=10, padx=10, fill="x")
home_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "staff_dashboard.py") if role_id == 2 else "admin_dashboard.py", user_email]) and manage_vehicles_window.destroy())

# Vehicle Management
vehicle_label = ctk.CTkLabel(sidebar_frame, text="Vehicle Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['vehicle'], compound="left", anchor="w", fg_color="#FFA500", width=200)
vehicle_label.pack(pady=10, padx=10, fill="x")

# Customer Management
customer_label = ctk.CTkLabel(sidebar_frame, text="Customer Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['customer'], compound="left", anchor="w", cursor="hand2")
customer_label.pack(pady=10, padx=10, fill="x")
customer_label.bind("<Button-1>", lambda event: subprocess.Popen(["python", "manage_customer.py", user_email]) and manage_vehicles_window.destroy())

# Rental History
history_label = ctk.CTkLabel(sidebar_frame, text="Bookings/Invoices", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['invoice'], compound="left", anchor="w", cursor="hand2")
history_label.pack(pady=10, padx=10, fill="x")
history_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "rental_history.py"), user_email]) and manage_vehicles_window.destroy())

# Reports
reports_label = ctk.CTkLabel(sidebar_frame, text="Reports", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['reports'], compound="left", anchor="w", cursor="hand2")
reports_label.pack(pady=10, padx=10, fill="x")
reports_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "reports.py"), user_email]) and manage_vehicles_window.destroy())

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>", lambda event: subprocess.Popen(["python", "login.py"]) and manage_vehicles_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(manage_vehicles_window, fg_color=COLORS['white'], width=800, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)

# Manage Vehicles title
manage_vehicles_title = ctk.CTkLabel(main_frame, text="Manage Vehicles", font=("Arial", 24, "bold"), text_color="black")
manage_vehicles_title.place(x=20, y=20)

# Table frame with scrollbar
table_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['white'], width=760, height=500, border_width=2, border_color="black")
table_frame.pack_propagate(False)
table_frame.place(x=20, y=60)

# Create a canvas and scrollbar for the table
canvas = tk.Canvas(table_frame, bg=COLORS['white'], highlightthickness=0)
scrollbar = ctk.CTkScrollbar(table_frame, orientation="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the table
table_inner_frame = ctk.CTkFrame(canvas, fg_color=COLORS['white'])
canvas.create_window((0, 0), window=table_inner_frame, anchor="nw")

# Pack the canvas and scrollbar
canvas.pack(side="top", fill="both", expand=True)
scrollbar.pack(side="bottom", fill="x")

# Table headers
headers = ["Vehicle ID", "Year", "License Plate", "Cost Per Day ($)", "Status"]
for col, header in enumerate(headers):
    header_label = ctk.CTkLabel(table_inner_frame, text=header, font=("Arial", 14, "bold"), text_color="black", fg_color=COLORS['color_2'], width=100)
    header_label.grid(row=0, column=col, padx=1, pady=5)
action_header = ctk.CTkLabel(table_inner_frame, text="Actions", font=("Arial", 14, "bold"), text_color="black", fg_color=COLORS['color_2'], width=120)
action_header.grid(row=0, column=len(headers), padx=1, pady=5)

# Function to validate license plate format
def validate_license_plate(license_plate):
    return len(license_plate) == 6 and license_plate.isalnum()

# Function to open edit window with scrollbar
def edit_vehicle(vehicle_data):
    edit_window = ctk.CTkToplevel(manage_vehicles_window)
    edit_window.title("Edit Vehicle")
    edit_window.geometry("500x600")
    edit_window.resizable(False, False)
    edit_window.transient(manage_vehicles_window)  # Make it modal
    edit_window.grab_set()

    # Create a canvas and scrollbar for the edit window
    canvas = tk.Canvas(edit_window, bg=COLORS['white'], highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(edit_window, orientation="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the form
    form_frame = ctk.CTkFrame(canvas, fg_color=COLORS['white'])
    canvas.create_window((0, 0), window=form_frame, anchor="nw")

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Form fields
    labels = ["Year", "License Plate", "Cost Per Day ($)", "Status"]
    entries = {}
    for i, label in enumerate(labels):
        ctk.CTkLabel(form_frame, text=label, font=("Arial", 14, "bold")).grid(row=i, column=0, padx=20, pady=(20 if i == 0 else 5), sticky="w")
        if label == "Status":
            entries[label] = ctk.CTkOptionMenu(form_frame, values=["available", "unavailable"], width=300, height=40, font=("Arial", 14))
        else:
            entries[label] = ctk.CTkEntry(form_frame, width=300, height=40, font=("Arial", 14))
        entries[label].grid(row=i, column=1, padx=20, pady=(20 if i == 0 else 5), sticky="w")

    # Populate fields with current data
    entries["Year"].insert(0, vehicle_data[1])
    entries["License Plate"].insert(0, vehicle_data[2])
    entries["Cost Per Day ($)"].insert(0, vehicle_data[3])
    entries["Status"].set(vehicle_data[4])

    # Save button
    def save_changes():
        vehicle_id = vehicle_data[0]
        year = entries["Year"].get().strip()
        license_plate = entries["License Plate"].get().strip()
        cost_per_day = entries["Cost Per Day ($)"].get().strip()
        status = entries["Status"].get()

        # Validation
        if not all([year, license_plate, cost_per_day]):
            messagebox.showerror("Error", "All required fields must be filled")
            return
        try:
            year = int(year)
            if year < 1900 or year > 2025:
                messagebox.showerror("Error", "Year must be between 1900 and 2025")
                return
        except ValueError:
            messagebox.showerror("Error", "Year must be a valid number")
            return
        if not validate_license_plate(license_plate):
            messagebox.showerror("Error", "License plate must be exactly 6 alphanumeric characters")
            return
        try:
            cost_per_day = float(cost_per_day)
            if cost_per_day <= 0:
                messagebox.showerror("Error", "Cost per day must be a positive number")
                return
        except ValueError:
            messagebox.showerror("Error", "Cost per day must be a valid number")
            return

        # Check if license plate is unique
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM vehicles WHERE license_plate = %s AND vehicle_id != %s", (license_plate, vehicle_id))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "License plate already exists")
                return

            # Update vehicle in the database
            cursor.execute(
                "UPDATE vehicles SET year = %s, license_plate = %s, cost_per_day = %s, status = %s WHERE vehicle_id = %s",
                (year, license_plate, cost_per_day, status, vehicle_id)
            )
            conn.commit()
            messagebox.showinfo("Success", "Vehicle updated successfully")
            edit_window.destroy()
            # Refresh the vehicle list
            subprocess.Popen(["python", "manage_vehicles.py", user_email])
            manage_vehicles_window.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to update vehicle: {e}")
        finally:
            cursor.close()
            conn.close()

    # Save Button
    save_button = ctk.CTkButton(form_frame, text="Save Changes", font=("Arial", 16, "bold"), fg_color=COLORS['sidebar'], text_color="white", width=300, height=50, command=save_changes)
    save_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

    # Update the canvas scroll region
    form_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function to toggle vehicle status (available/unavailable)
def toggle_status(vehicle_id, current_status):
    new_status = "unavailable" if current_status == "available" else "available"
    if not messagebox.askyesno("Confirm", f"Are you sure you want to set this vehicle to '{new_status}'?"):
        return
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE vehicles SET status = %s WHERE vehicle_id = %s", (new_status, vehicle_id))
        conn.commit()
        messagebox.showinfo("Success", f"Vehicle status set to '{new_status}' successfully")
        # Refresh the vehicle list
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_vehicles.py"), user_email])
        manage_vehicles_window.destroy()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to update vehicle status: {e}")
    finally:
        cursor.close()
        conn.close()

# Fetch and display vehicles
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT vehicle_id, year, license_plate, cost_per_day, status
        FROM vehicles
    """
    cursor.execute(query)
    vehicles = cursor.fetchall()

    # Map the indices to the displayed columns
    display_indices = [0, 1, 2, 3, 4]
    for row, vehicle in enumerate(vehicles, start=1):
        for col, idx in enumerate(display_indices):
            cell_label = ctk.CTkLabel(table_inner_frame, text=str(vehicle[idx]) if vehicle[idx] else "", font=("Arial", 12), text_color="black", width=100)
            cell_label.grid(row=row, column=col, padx=1, pady=2)
        # Action buttons
        action_frame = ctk.CTkFrame(table_inner_frame, fg_color=COLORS['white'])
        action_frame.grid(row=row, column=len(display_indices), padx=5, pady=2)
        edit_button = ctk.CTkButton(action_frame, text="Edit", font=("Arial", 12, "bold"), fg_color="blue", text_color="white", width=50, height=30, command=lambda v=vehicle: edit_vehicle(v))
        edit_button.pack(side="left", padx=2)
        # Available/Unavailable button based on current status
        status = vehicle[4]
        button_text = "Set Unavailable" if status == "available" else "Set Available"
        button_color = "red" if status == "available" else "green"
        status_button = ctk.CTkButton(action_frame, text=button_text, font=("Arial", 12, "bold"), fg_color=button_color, text_color="white", width=50, height=30, command=lambda v_id=vehicle[0], s=status: toggle_status(v_id, s))
        status_button.pack(side="left", padx=2)

    # Update the canvas scroll region for the table
    table_inner_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

except Exception as e:
    messagebox.showerror("Error", f"Failed to fetch vehicles: {e}")
    manage_vehicles_window.destroy()
    sys.exit(1)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

manage_vehicles_window.mainloop()