# staff_dashboard.py
import sys
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection
from constants import COLORS
import subprocess
import sys
from PIL import Image
from datetime import datetime

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

staff_email = sys.argv[1] if len(sys.argv) > 1 else "staff@example.com"

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

# Validate that the user is a staff member (role_id = 2)
role_id = get_user_role(staff_email)
if role_id != 2:  # Only staff (role_id = 2) can access this page
    messagebox.showerror("Error", "Unauthorized access: Only staff members can access the Staff Dashboard.")
    sys.exit(1)

staff_dashboard_window = ctk.CTk()
staff_dashboard_window.title("Staff Dashboard - QuickDrive Rentals")
staff_dashboard_window.geometry("800x600")
staff_dashboard_window.resizable(False, False)
staff_dashboard_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(staff_dashboard_window, fg_color=COLORS['color_1'], width=250, height=600)
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
home_label = ctk.CTkLabel(sidebar_frame, text="Home", font=("Arial", 16, "bold"), text_color="black",
                          image=nav_icons['home'], compound="left", anchor="w", fg_color="#FFA500", width=200)
home_label.pack(pady=10, padx=10, fill="x")

# Vehicle Management
vehicle_label = ctk.CTkLabel(sidebar_frame, text="Vehicle Management", font=("Arial", 16, "bold"), text_color="black",
                             image=nav_icons['vehicle'], compound="left", anchor="w", cursor="hand2")
vehicle_label.pack(pady=10, padx=10, fill="x")
vehicle_label.bind("<Button-1>", lambda event: subprocess.Popen(
    [sys.executable, os.path.join(os.getcwd(), "manage_vehicle.py"), staff_email]) and staff_dashboard_window.destroy())

# Customer Management
customer_label = ctk.CTkLabel(sidebar_frame, text="Customer Management", font=("Arial", 16, "bold"), text_color="black",
                              image=nav_icons['customer'], compound="left", anchor="w", cursor="hand2")
customer_label.pack(pady=10, padx=10, fill="x")
customer_label.bind("<Button-1>", lambda event: subprocess.Popen(
    [sys.executable, os.path.join(os.getcwd(), "manage_customer.py"), staff_email]) and staff_dashboard_window.destroy())

# Rental History
history_label = ctk.CTkLabel(sidebar_frame, text="Bookings/Invoices", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['invoice'], compound="left", anchor="w", cursor="hand2")
history_label.pack(pady=10, padx=10, fill="x")
history_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "rental_history.py"), staff_email]) and staff_dashboard_window.destroy())

# Reports
reports_label = ctk.CTkLabel(sidebar_frame, text="Reports", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['reports'], compound="left", anchor="w", cursor="hand2")
reports_label.pack(pady=10, padx=10, fill="x")
reports_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "reports.py"), staff_email]) and staff_dashboard_window.destroy())

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black",
                            image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>",
                  lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")]) and staff_dashboard_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(staff_dashboard_window, fg_color="white", width=600, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)


# Retrieve staff's name from the database
def get_staff_name(email):
    conn = get_db_connection()
    if not conn:
        return "Staff"

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT first_name, last_name FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return f"{user[0].capitalize()} {user[1].capitalize()}"
        return "Staff"
    except Exception as e:
        print(f"Error retrieving staff name: {e}")
        return "Staff"
    finally:
        cursor.close()
        conn.close()


staff_name = get_staff_name(staff_email)

# Welcome message
welcome_label = ctk.CTkLabel(main_frame, text=f"Welcome, {staff_name}!", font=("Arial", 20, "bold"), text_color="black")
welcome_label.place(x=20, y=20)


# Fetch real-time statistics from the database
def fetch_statistics():
    conn = get_db_connection()
    if not conn:
        return {
            "total_vehicles": 0,
            "active_bookings": 0,
            "revenue": 0.0,
            "avg_rate": 0.0,
            "monthly_revenue": 0.0
        }

    cursor = conn.cursor()
    stats = {}

    try:
        # Total Vehicles
        cursor.execute("SELECT COUNT(*) FROM vehicles")
        stats["total_vehicles"] = cursor.fetchone()[0]

        # Active Bookings
        cursor.execute("SELECT COUNT(*) FROM rentals WHERE status = 'active'")
        stats["active_bookings"] = cursor.fetchone()[0]

        # Revenue (total from completed rentals)
        cursor.execute("SELECT SUM(total_cost) FROM rentals WHERE status = 'completed'")
        revenue = cursor.fetchone()[0]
        stats["revenue"] = revenue if revenue else 0.0

        # Average Rate (average total_cost of completed rentals)
        cursor.execute("SELECT AVG(total_cost) FROM rentals WHERE status = 'completed'")
        avg_rate = cursor.fetchone()[0]
        stats["avg_rate"] = round(avg_rate, 2) if avg_rate else 0.0

        # Monthly Revenue (completed rentals in the current month)
        current_month = datetime.now().strftime('%Y-%m')
        cursor.execute(
            "SELECT SUM(total_cost) FROM rentals WHERE status = 'completed' AND DATE_FORMAT(end_date, '%Y-%m') = %s",
            (current_month,))
        monthly_revenue = cursor.fetchone()[0]
        stats["monthly_revenue"] = monthly_revenue if monthly_revenue else 0.0

    except Exception as e:
        print(f"Error fetching statistics: {e}")
        stats = {
            "total_vehicles": 0,
            "active_bookings": 0,
            "revenue": 0.0,
            "avg_rate": 0.0,
            "monthly_revenue": 0.0
        }
    finally:
        cursor.close()
        conn.close()

    return stats


# Fetch statistics
stats = fetch_statistics()

# Quick Statistics section
stats_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['color_2'], width=460, height=220)
stats_frame.pack_propagate(False)
stats_frame.place(x=20, y=60)

stats_header = ctk.CTkLabel(stats_frame, text="Quick Statistics", font=("Arial", 16, "bold"), text_color="black",
                            fg_color=COLORS['color_2'], width=560)
stats_header.pack(pady=0)

# Stats content
stats_date = ctk.CTkLabel(stats_frame, text=f"{datetime.now().strftime('%A, %B %d, %Y')}", font=("Arial", 14),
                          text_color="black")
stats_date.pack(pady=4)

stats_total_vehicles = ctk.CTkLabel(stats_frame, text=f"Total Vehicles: {stats['total_vehicles']}", font=("Arial", 14),
                                    text_color="black")
stats_total_vehicles.pack(pady=3)

stats_active_bookings = ctk.CTkLabel(stats_frame, text=f"Active Bookings: {stats['active_bookings']}",
                                     font=("Arial", 14), text_color="black")
stats_active_bookings.pack(pady=3)

stats_revenue = ctk.CTkLabel(stats_frame, text=f"Revenue: ${stats['revenue']:,.2f}", font=("Arial", 14),
                             text_color="black")
stats_revenue.pack(pady=3)

stats_avg_rate = ctk.CTkLabel(stats_frame, text=f"Average Rate: ${stats['avg_rate']:,.2f}", font=("Arial", 14),
                              text_color="black")
stats_avg_rate.pack(pady=3)

stats_monthly_revenue = ctk.CTkLabel(stats_frame, text=f"Monthly Revenue: ${stats['monthly_revenue']:,.2f}",
                                     font=("Arial", 14), text_color="black")
stats_monthly_revenue.pack(pady=3)

# Action buttons
action_icons = {
    "add_vehicle": ctk.CTkImage(light_image=Image.open("images/add_vehicle_icon.png"), size=(50, 50)),
    "view_booking": ctk.CTkImage(light_image=Image.open("images/view_booking_icon.png"), size=(50, 50)),
    "manage_customer": ctk.CTkImage(light_image=Image.open("images/manage_customer_icon.png"), size=(50, 50)),
    "book_vehicle": ctk.CTkImage(light_image=Image.open("images/book_vehicle_icon.png"), size=(50, 50))
}

# Add Vehicle button
add_vehicle_button = ctk.CTkButton(main_frame, text="Add Vehicle", font=("Arial", 16, "bold"), fg_color="#E8E5DB",
                                   text_color="black", image=action_icons['add_vehicle'], compound="left",
                                   border_width=2, border_color="black", width=200, height=100,
                                   command=lambda: subprocess.Popen(
                                       [sys.executable, os.path.join(os.getcwd(), "add_vehicle.py"), staff_email]) and staff_dashboard_window.destroy())
add_vehicle_button.place(x=20, y=300)

# View Booking button
view_booking_button = ctk.CTkButton(main_frame, text="View Booking", font=("Arial", 16, "bold"), fg_color="#E8E5DB",
                                    text_color="black", image=action_icons['view_booking'], compound="left",
                                    border_width=2, border_color="black", width=200, height=100,
                                    command=lambda: subprocess.Popen(
                                        [sys.executable, os.path.join(os.getcwd(), "view_bookings.py"), staff_email]) and staff_dashboard_window.destroy())
view_booking_button.place(x=330, y=300)

# Manage Customer button
manage_customer_button = ctk.CTkButton(main_frame, text="Manage Customer", font=("Arial", 16, "bold"),
                                       fg_color="#E8E5DB", text_color="black", image=action_icons['manage_customer'],
                                       compound="left", border_width=2, border_color="black", width=200, height=100,
                                       command=lambda: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_customer.py"),
                                                                         staff_email]) and staff_dashboard_window.destroy())
manage_customer_button.place(x=330, y=450)

# Manage Customer button
book_vehicle_button = ctk.CTkButton(main_frame, text="Book a Vehicle", font=("Arial", 16, "bold"),
                                       fg_color="#E8E5DB", text_color="black", image=action_icons['book_vehicle'],
                                       compound="left", border_width=2, border_color="black", width=200, height=100,
                                       command=lambda: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "book_vehicle.py"),
                                                                         staff_email]) and staff_dashboard_window.destroy())
book_vehicle_button.place(x=20, y=450)

staff_dashboard_window.mainloop()