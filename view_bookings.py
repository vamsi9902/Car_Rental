# view_bookings.py
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection
from constants import COLORS
import subprocess
import sys
import os
from PIL import Image
from datetime import datetime

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
if role_id is None:
    messagebox.showerror("Error", "Unauthorized access")
    sys.exit(1)
is_customer = role_id == 3  # Role ID 3 is for customers

# Initialize the main window
view_bookings_window = ctk.CTk()
view_bookings_window.title("View Bookings - QuickDrive Rentals")
view_bookings_window.geometry("1200x600")
view_bookings_window.resizable(False, False)
view_bookings_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(view_bookings_window, fg_color=COLORS['color_1'], width=250, height=600)
sidebar_frame.pack_propagate(False)
sidebar_frame.place(x=0, y=0)

# Sidebar navigation options (with larger icons)
nav_icons = {
    "home": ctk.CTkImage(light_image=Image.open("images/home_icon.png"), size=(50, 50)),
    "vehicle": ctk.CTkImage(light_image=Image.open("images/vehicle_icon.png"), size=(50, 50)),
    "customer": ctk.CTkImage(light_image=Image.open("images/customer_icon.png"), size=(50, 50)),
    "invoice": ctk.CTkImage(light_image=Image.open("images/invoice.png"), size=(50, 50)),
    "reports": ctk.CTkImage(light_image=Image.open("images/reports_icon.png"), size=(50, 50)),
    "logout": ctk.CTkImage(light_image=Image.open("images/logout_icon.png"), size=(50, 50))
}

# Home
dashboard_script = "customer_dashboard.py" if is_customer else "staff_dashboard.py" if role_id == 2 else "admin_dashboard.py"
home_label = ctk.CTkLabel(sidebar_frame, text="Home", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['home'], compound="left", anchor="w", cursor="hand2")
home_label.pack(pady=10, padx=10, fill="x")
home_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), dashboard_script), user_email]) and view_bookings_window.destroy())

# Admin/Staff-specific sidebar options
if not is_customer:
    # Vehicle Management
    vehicle_label = ctk.CTkLabel(sidebar_frame, text="Vehicle Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['vehicle'], compound="left", anchor="w", cursor="hand2")
    vehicle_label.pack(pady=10, padx=10, fill="x")
    vehicle_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_vehicle.py"), user_email]) and view_bookings_window.destroy())

    # Customer Management
    customer_label = ctk.CTkLabel(sidebar_frame, text="Customer Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['customer'], compound="left", anchor="w", cursor="hand2")
    customer_label.pack(pady=10, padx=10, fill="x")
    customer_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_customer.py"), user_email]) and view_bookings_window.destroy())

    # Rental History
    history_label = ctk.CTkLabel(sidebar_frame, text="Bookings/Invoices", font=("Arial", 16, "bold"),
                                 text_color="black", image=nav_icons['invoice'], compound="left", anchor="w",
                                 cursor="hand2")
    history_label.pack(pady=10, padx=10, fill="x")
    history_label.bind("<Button-1>", lambda event: subprocess.Popen(
        [sys.executable, os.path.join(os.getcwd(), "rental_history.py"),
         user_email]) and view_bookings_window.destroy())

    # Reports
    reports_label = ctk.CTkLabel(sidebar_frame, text="Reports", font=("Arial", 16, "bold"), text_color="black",
                                 image=nav_icons['reports'], compound="left", anchor="w", cursor="hand2")
    reports_label.pack(pady=10, padx=10, fill="x")
    reports_label.bind("<Button-1>", lambda event: subprocess.Popen(
        [sys.executable, os.path.join(os.getcwd(), "reports.py"), user_email]) and view_bookings_window.destroy())

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")]) and view_bookings_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(view_bookings_window, fg_color=COLORS['white'], width=950, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)

# View Bookings title
view_bookings_title = ctk.CTkLabel(main_frame, text="View Bookings", font=("Arial", 24, "bold"), text_color="black")
view_bookings_title.place(x=20, y=20)

# Table frame
table_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['white'], width=950, height=500, border_width=2, border_color="black")
table_frame.pack_propagate(False)
table_frame.place(x=20, y=60)

# Header frame
header_frame = ctk.CTkFrame(table_frame, fg_color=COLORS['white'], width=950, height=40)
header_frame.pack_propagate(False)
header_frame.pack(side="top", fill="x")

# Data frame
data_frame = ctk.CTkFrame(table_frame, fg_color=COLORS['white'], width=950, height=460)
data_frame.pack_propagate(False)
data_frame.pack(side="top", fill="both", expand=True)

# Create a canvas with horizontal scrollbar inside the data frame
canvas = tk.Canvas(data_frame, bg=COLORS['white'], highlightthickness=0)
scrollbar = ctk.CTkScrollbar(data_frame, orientation="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the table data
table_inner_frame = ctk.CTkFrame(canvas, fg_color=COLORS['white'])
canvas.create_window((0, 0), window=table_inner_frame, anchor="nw")

# Pack the canvas and scrollbar
canvas.pack(side="top", fill="both", expand=True)
scrollbar.pack(side="bottom", fill="x")

# Table headers
headers = ["Rental ID", "Customer Name", "Vehicle", "Start Date", "End Date", "Total Cost", "Status"]
for col, header in enumerate(headers):
    header_label = ctk.CTkLabel(
        header_frame,
        text=header,
        font=("Arial", 14, "bold"),
        text_color="black",
        fg_color=COLORS['color_2'],
        width=100,
        anchor="center"
    )
    header_label.grid(row=0, column=col, padx=3, pady=5)

action_header = ctk.CTkLabel(
    header_frame,
    text="Actions",
    font=("Arial", 14, "bold"),
    text_color="black",
    fg_color=COLORS['color_2'],
    width=120,
    anchor="center"
)
action_header.grid(row=0, column=len(headers), padx=1, pady=5)

# Function to validate date format (YYYY-MM-DD)
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Function to open edit window for a booking
def edit_booking(booking_data):
    edit_window = ctk.CTkToplevel(view_bookings_window)
    edit_window.title("Edit Booking")
    window_height = 320 if is_customer else 400
    edit_window.geometry(f"600x{window_height}")
    edit_window.resizable(False, False)
    edit_window.transient(view_bookings_window)
    edit_window.grab_set()

    # Form fields (different for customers vs admin/staff)
    if is_customer:
        labels = ["Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"]
    else:
        labels = ["Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)", "Status"]

    entries = {}
    for i, label in enumerate(labels):
        ctk.CTkLabel(edit_window, text=label, font=("Arial", 14, "bold")).grid(row=i, column=0, padx=20, pady=(20 if i == 0 else 5), sticky="w")
        if label == "Status":
            entries[label] = ctk.CTkOptionMenu(edit_window, values=["active", "completed", "cancelled"], width=300, height=40, font=("Arial", 14))
        else:
            entries[label] = ctk.CTkEntry(edit_window, width=300, height=40, font=("Arial", 14))
        entries[label].grid(row=i, column=1, padx=20, pady=(20 if i == 0 else 5), sticky="w")

    # Populate fields with current data
    entries["Start Date (YYYY-MM-DD)"].insert(0, booking_data[3])
    entries["End Date (YYYY-MM-DD)"].insert(0, booking_data[4])
    if not is_customer and "Status" in entries:
        entries["Status"].set(booking_data[6])

    # Save button
    def save_changes():
        rental_id = booking_data[0]
        start_date = entries["Start Date (YYYY-MM-DD)"].get().strip()
        end_date = entries["End Date (YYYY-MM-DD)"].get().strip()
        # Use existing status for customers; for admin/staff, get from dropdown
        status = booking_data[6] if is_customer else entries["Status"].get()

        # Validation
        if not all([start_date, end_date]):
            messagebox.showerror("Error", "All required fields must be filled")
            return
        if not validate_date(start_date) or not validate_date(end_date):
            messagebox.showerror("Error", "Invalid date format (use YYYY-MM-DD)")
            return
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date_obj > end_date_obj:
                messagebox.showerror("Error", "End date must be after start date")
                return

            # Recalculate total cost based on new dates
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT v.cost_per_day FROM vehicles v JOIN rentals r ON v.vehicle_id = r.vehicle_id WHERE r.rental_id = %s", (rental_id,))
            cost_per_day = cursor.fetchone()[0]
            days = (end_date_obj - start_date_obj).days + 1
            total_cost = days * cost_per_day

            # Update booking
            cursor.execute(
                "UPDATE rentals SET start_date = %s, end_date = %s, total_cost = %s, status = %s WHERE rental_id = %s",
                (start_date, end_date, total_cost, status, rental_id)
            )
            # Update vehicle status if booking status changes (only applies for admin/staff)
            if not is_customer:
                if status == "completed" or status == "cancelled":
                    cursor.execute("UPDATE vehicles v JOIN rentals r ON v.vehicle_id = r.vehicle_id SET v.status = 'available' WHERE r.rental_id = %s", (rental_id,))
                elif status == "active":
                    cursor.execute("UPDATE vehicles v JOIN rentals r ON v.vehicle_id = r.vehicle_id SET v.status = 'rented' WHERE r.rental_id = %s", (rental_id,))
            conn.commit()
            messagebox.showinfo("Success", "Booking updated successfully")
            edit_window.destroy()
            # Refresh the bookings list
            subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "view_bookings.py"), user_email])
            view_bookings_window.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to update booking: {e}")
        finally:
            cursor.close()
            conn.close()

    save_button_y = 240 if is_customer else 320
    save_button = ctk.CTkButton(edit_window, text="Save Changes", font=("Arial", 16, "bold"), fg_color=COLORS['color_1'], text_color="white", width=300, height=50, command=save_changes)
    save_button.place(x=130, y=save_button_y)

# Function to cancel a booking
def cancel_booking(rental_id):
    if not messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?"):
        return
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE rentals SET status = 'cancelled' WHERE rental_id = %s", (rental_id,))
        cursor.execute("UPDATE vehicles v JOIN rentals r ON v.vehicle_id = r.vehicle_id SET v.status = 'available' WHERE r.rental_id = %s", (rental_id,))
        conn.commit()
        messagebox.showinfo("Success", "Booking cancelled successfully")
        # Refresh the bookings list
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "view_bookings.py"), user_email])
        view_bookings_window.destroy()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to cancel booking: {e}")
    finally:
        cursor.close()
        conn.close()

# Fetch and display bookings
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    if is_customer:
        # Fetch customer_id for the logged-in customer
        cursor.execute("""
            SELECT c.customer_id
            FROM customers c
            JOIN users u ON c.user_id = u.user_id
            WHERE u.email = %s
        """, (user_email,))
        customer = cursor.fetchone()
        if not customer:
            messagebox.showerror("Error", "Customer not found for this email")
            cursor.close()
            conn.close()
            sys.exit(1)
        customer_id = customer[0]
        # Fetch active or upcoming bookings for this customer
        query = """
            SELECT r.rental_id, CONCAT(u.first_name, ' ', u.last_name) AS customer_name,
                   CONCAT(v.make, ' ', v.model, ' (', v.license_plate, ')') AS vehicle,
                   r.start_date, r.end_date, r.total_cost, r.status
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN users u ON c.user_id = u.user_id
            JOIN vehicles v ON r.vehicle_id = v.vehicle_id
            WHERE r.customer_id = %s AND (r.status = 'active' OR r.end_date >= CURDATE())
            ORDER BY r.start_date DESC
        """
        cursor.execute(query, (customer_id,))
    else:
        # Fetch all active or upcoming bookings for admin/staff
        query = """
            SELECT r.rental_id, CONCAT(u.first_name, ' ', u.last_name) AS customer_name,
                   CONCAT(v.make, ' ', v.model, ' (', v.license_plate, ')') AS vehicle,
                   r.start_date, r.end_date, r.total_cost, r.status
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN users u ON c.user_id = u.user_id
            JOIN vehicles v ON r.vehicle_id = v.vehicle_id
            WHERE r.status = 'active' OR r.end_date >= CURDATE()
            ORDER BY r.start_date DESC
        """
        cursor.execute(query)

    bookings = cursor.fetchall()

    # Display bookings in the table
    display_indices = [0, 1, 2, 3, 4, 5, 6]
    for row, booking in enumerate(bookings, start=1):
        for col, idx in enumerate(display_indices):
            value = booking[idx]
            if idx == 5:
                value = f"${float(value):.2f}"
            else:
                value = str(value)
            cell_label = ctk.CTkLabel(table_inner_frame, text=value, font=("Arial", 12), text_color="black", width=100, anchor="center")
            cell_label.grid(row=row, column=col, padx=1, pady=2)
        # Action buttons
        action_frame = ctk.CTkFrame(table_inner_frame, fg_color=COLORS['white'])
        action_frame.grid(row=row, column=len(display_indices), padx=5, pady=2)
        edit_button = ctk.CTkButton(action_frame, text="Edit", font=("Arial", 12, "bold"), fg_color="blue", text_color="white", width=50, height=30, command=lambda b=booking: edit_booking(b))
        edit_button.pack(side="left", padx=2)
        cancel_button = ctk.CTkButton(action_frame, text="Cancel", font=("Arial", 12, "bold"), fg_color="red", text_color="white", width=50, height=30, command=lambda r_id=booking[0]: cancel_booking(r_id))
        cancel_button.pack(side="left", padx=2)

    # If no bookings, display a message
    if not bookings:
        no_bookings_label = ctk.CTkLabel(table_inner_frame, text="No active or upcoming bookings found.", font=("Arial", 14), text_color="black")
        no_bookings_label.grid(row=1, column=0, columnspan=len(headers) + 1, pady=20)

    # Update the canvas scroll region
    table_inner_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

except Exception as e:
    messagebox.showerror("Error", f"Failed to fetch bookings: {e}")
    view_bookings_window.destroy()
    sys.exit(1)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

view_bookings_window.mainloop()