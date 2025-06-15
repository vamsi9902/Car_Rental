# book_vehicle.py
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection
from constants import COLORS
import subprocess
import sys
from datetime import datetime
import os
from PIL import Image
from tkcalendar import Calendar

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
if role_id is None:
    messagebox.showerror("Error", "Unauthorized access")
    sys.exit(1)
is_customer = role_id == 3

# Initialize the main window
book_vehicle_window = ctk.CTk()
book_vehicle_window.title("Book a Vehicle - QuickDrive Rentals")
book_vehicle_window.geometry("850x600")
book_vehicle_window.resizable(False, False)
book_vehicle_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(book_vehicle_window, fg_color=COLORS['color_1'], width=250, height=600)
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
dashboard_script = "customer_dashboard.py" if is_customer else "staff_dashboard.py" if role_id == 2 else "admin_dashboard.py"
home_label = ctk.CTkLabel(sidebar_frame, text="Home", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['home'], compound="left", anchor="w", cursor="hand2")
home_label.pack(pady=10, padx=10, fill="x")
home_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), dashboard_script), user_email]) and book_vehicle_window.destroy())

# Admin/Staff-specific sidebar options
if not is_customer:
    # Vehicle Management
    vehicle_label = ctk.CTkLabel(sidebar_frame, text="Vehicle Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['vehicle'], compound="left", anchor="w", cursor="hand2")
    vehicle_label.pack(pady=10, padx=10, fill="x")
    vehicle_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_vehicle.py"), user_email]) and book_vehicle_window.destroy())

    # Customer Management
    customer_label = ctk.CTkLabel(sidebar_frame, text="Customer Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['customer'], compound="left", anchor="w", cursor="hand2")
    customer_label.pack(pady=10, padx=10, fill="x")
    customer_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_customer.py"), user_email]) and book_vehicle_window.destroy())

    # Rental History
    history_label = ctk.CTkLabel(sidebar_frame, text="Bookings/Invoices", font=("Arial", 16, "bold"),
                                 text_color="black", image=nav_icons['customer'], compound="left", anchor="w",
                                 cursor="hand2")
    history_label.pack(pady=10, padx=10, fill="x")
    history_label.bind("<Button-1>", lambda event: subprocess.Popen(
        [sys.executable, os.path.join(os.getcwd(), "rental_history.py"),
         user_email]) and book_vehicle_window.destroy())

    # Reports
    reports_label = ctk.CTkLabel(sidebar_frame, text="Reports", font=("Arial", 16, "bold"), text_color="black",
                                 image=nav_icons['reports'], compound="left", anchor="w", cursor="hand2")
    reports_label.pack(pady=10, padx=10, fill="x")
    reports_label.bind("<Button-1>", lambda event: subprocess.Popen(
        [sys.executable, os.path.join(os.getcwd(), "reports.py"), user_email]) and book_vehicle_window.destroy())

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")]) and book_vehicle_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(book_vehicle_window, fg_color=COLORS['white'], width=600, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)

# Book a Vehicle title
book_vehicle_title = ctk.CTkLabel(main_frame, text="Book a Vehicle", font=("Arial", 24, "bold"), text_color="black")
book_vehicle_title.place(x=20, y=20)

# Form frame
form_frame = ctk.CTkScrollableFrame(main_frame, fg_color=COLORS['white'], width=560, height=500)
form_frame.pack_propagate(False)
form_frame.place(x=20, y=60)

# Function to open a calendar popup and set the selected date in the entry
def open_calendar(entry, button):
    # Check if a calendar is already open
    if hasattr(entry, 'calendar_popup') and entry.calendar_popup.winfo_exists():
        entry.calendar_popup.destroy()

    def set_date():
        selected_date = cal.get_date()
        entry.delete(0, tk.END)
        entry.insert(0, selected_date)
        top.destroy()
        update_vehicle_details()

    def on_focus_out(event):
        # Close the calendar if focus is lost
        if not top.focus_get():
            top.destroy()

    # Create the popup window
    top = tk.Toplevel(book_vehicle_window)
    entry.calendar_popup = top
    top.overrideredirect(True)
    top.configure(bg="white")

    button_x = button.winfo_rootx()
    button_y = button.winfo_rooty()
    button_height = button.winfo_height()

    popup_width = 350
    popup_height = 350
    top.geometry(f"{popup_width}x{popup_height}+{button_x}+{button_y + button_height}")

    # Add the calendar widget
    cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 10), background="white", foreground="black")
    cal.pack(pady=5)

    # Add the Select button
    select_button = ctk.CTkButton(top, text="Select", command=set_date, font=("Arial", 14), fg_color="green", text_color="white", width=100, height=30)
    select_button.pack(pady=5)

    # Bind focus out event to close the popup
    top.bind("<FocusOut>", on_focus_out)

    top.transient(book_vehicle_window)
    top.grab_set()
    top.focus_set()

# Function to validate date format
def validate_date(date_str):
    if not date_str:  # Allow empty strings
        return True
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Date Selection with Calendar
ctk.CTkLabel(form_frame, text="Start Date (YYYY-MM-DD)", font=("Arial", 16, "bold"), text_color="black").grid(row=0, column=0, padx=20, pady=10, sticky="w")
start_date_entry = ctk.CTkEntry(form_frame, width=300, height=40, font=("Arial", 14), placeholder_text="e.g., 2025-01-01")
start_date_entry.grid(row=1, column=0, padx=20, pady=5, sticky="w")
start_date_button = ctk.CTkButton(form_frame, text="📅", font=("Arial", 14), width=40, height=40, fg_color="darkblue", text_color="white", command=lambda: open_calendar(start_date_entry, start_date_button))
start_date_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

ctk.CTkLabel(form_frame, text="End Date (YYYY-MM-DD)", font=("Arial", 16, "bold"), text_color="black").grid(row=2, column=0, padx=20, pady=10, sticky="w")
end_date_entry = ctk.CTkEntry(form_frame, width=300, height=40, font=("Arial", 14), placeholder_text="e.g., 2025-12-31")
end_date_entry.grid(row=3, column=0, padx=20, pady=5, sticky="w")
end_date_button = ctk.CTkButton(form_frame, text="📅", font=("Arial", 14), width=40, height=40, fg_color="darkblue", text_color="white", command=lambda: open_calendar(end_date_entry, end_date_button))
end_date_button.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Bind validation to date entries
def on_date_change(*args):
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    if start_date and not validate_date(start_date):
        messagebox.showerror("Error", "Start Date must be in YYYY-MM-DD format (e.g., 2025-01-01)")
        start_date_entry.delete(0, tk.END)
    if end_date and not validate_date(end_date):
        messagebox.showerror("Error", "End Date must be in YYYY-MM-DD format (e.g., 2025-12-31)")
        end_date_entry.delete(0, tk.END)
    update_vehicle_details()

start_date_entry.bind("<KeyRelease>", on_date_change)
end_date_entry.bind("<KeyRelease>", on_date_change)

# List of Vehicles
ctk.CTkLabel(form_frame, text="List of Vehicles", font=("Arial", 16, "bold"), text_color="black").grid(row=4, column=0, padx=20, pady=10, sticky="w")
vehicles_dropdown = ctk.CTkComboBox(form_frame, width=300, height=40, font=("Arial", 14), command=lambda _: update_vehicle_details())
vehicles_dropdown.grid(row=5, column=0, padx=20, pady=5, sticky="w")

# Vehicle Details
vehicle_details_label = ctk.CTkLabel(form_frame, text="Vehicle Details:", font=("Arial", 16, "bold"), text_color="black")
vehicle_details_label.grid(row=4, column=1, padx=20, pady=10, sticky="w")
make_label = ctk.CTkLabel(form_frame, text="Make: ", font=("Arial", 14), text_color="black")
make_label.grid(row=5, column=1, padx=20, pady=2, sticky="w")
model_label = ctk.CTkLabel(form_frame, text="Model: ", font=("Arial", 14), text_color="black")
model_label.grid(row=6, column=1, padx=20, pady=2, sticky="w")
year_label = ctk.CTkLabel(form_frame, text="Year: ", font=("Arial", 14), text_color="black")
year_label.grid(row=7, column=1, padx=20, pady=2, sticky="w")

# Cost breakdown labels
cost_per_day_label = ctk.CTkLabel(form_frame, text="Cost Per Day:", font=("Arial", 14, "bold"), text_color="black")
cost_per_day_label.grid(row=14, column=1, padx=20, pady=5, sticky="w")
cost_per_day_value = ctk.CTkLabel(form_frame, text="$0.00", font=("Arial", 14), text_color="black")
cost_per_day_value.grid(row=14, column=1, padx=20, pady=5, sticky="e")

total_cost_label = ctk.CTkLabel(form_frame, text="Total Cost:", font=("Arial", 14, "bold"), text_color="black")
total_cost_label.grid(row=15, column=1, padx=20, pady=5, sticky="w")
total_cost_value = ctk.CTkLabel(form_frame, text="$0.00", font=("Arial", 14), text_color="black")
total_cost_value.grid(row=15, column=1, padx=20, pady=5, sticky="e")

taxes_label = ctk.CTkLabel(form_frame, text="Taxes (6%):", font=("Arial", 14, "bold"), text_color="red")
taxes_label.grid(row=16, column=1, padx=20, pady=5, sticky="w")
taxes_value = ctk.CTkLabel(form_frame, text="$0.00", font=("Arial", 14), text_color="red")
taxes_value.grid(row=16, column=1, padx=20, pady=5, sticky="e")

# Discount (only for admin/staff)
discount_var = tk.StringVar(value="0%")
if not is_customer:  # Only show discount for admin/staff
    discount_label = ctk.CTkLabel(form_frame, text="Discount:", font=("Arial", 14, "bold"), text_color="green")
    discount_label.grid(row=17, column=1, padx=20, pady=5, sticky="w")
    discount_dropdown = ctk.CTkOptionMenu(form_frame, values=["0%", "5%", "10%", "15%", "20%"], variable=discount_var, font=("Arial", 14), fg_color=COLORS['color_2'], text_color="black", width=100, height=30, command=lambda _: update_vehicle_details())
    discount_dropdown.grid(row=17, column=1, padx=20, pady=5, sticky="e")
    discount_value = ctk.CTkLabel(form_frame, text="$0.00", font=("Arial", 14), text_color="green")
    discount_value.grid(row=18, column=1, padx=20, pady=5, sticky="e")

# Adjust the "Total" label position based on whether discount is shown
total_row = 17 if is_customer else 19
final_total_label = ctk.CTkLabel(form_frame, text="Total:", font=("Arial", 14, "bold"), text_color="black")
final_total_label.grid(row=total_row, column=1, padx=20, pady=5, sticky="w")
final_total_value = ctk.CTkLabel(form_frame, text="$0.00", font=("Arial", 14), text_color="black")
final_total_value.grid(row=total_row, column=1, padx=20, pady=5, sticky="e")

# Fetch available vehicles
def fetch_vehicles():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT vehicle_id, license_plate, year, cost_per_day, make, model FROM vehicles WHERE status = 'available'")
        vehicles = cursor.fetchall()
        cursor.close()
        conn.close()
        return [(v[0], v[1], v[2], float(v[3]), v[4], v[5]) for v in vehicles]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch vehicles: {e}")
        return []

vehicles = fetch_vehicles()
vehicle_dict = {f"{v[4]} {v[5]} ({v[1]})": v for v in vehicles}
vehicles_dropdown.configure(values=list(vehicle_dict.keys()))
if vehicle_dict:
    vehicles_dropdown.set(list(vehicle_dict.keys())[0])
else:
    vehicles_dropdown.set("No vehicles available")

# Customer Details
customer_details_label = ctk.CTkLabel(form_frame, text="Customer Details:", font=("Arial", 16, "bold"), text_color="black")
customer_details_label.grid(row=8, column=0, padx=20, pady=10, sticky="w")

labels = ["First Name", "Last Name", "Email", "Phone Number", "Driving License Number"]
entries = {}
for i, label in enumerate(labels):
    ctk.CTkLabel(form_frame, text=label, font=("Arial", 14, "bold"), text_color="black").grid(row=(9 if i < 2 else 11 if i < 4 else 13), column=(0 if i % 2 == 0 else 1), padx=20, pady=5, sticky="w")
    entries[label] = ctk.CTkEntry(form_frame, width=200, height=40, border_color="black", border_width=1, font=("Arial", 14))
    entries[label].grid(row=(10 if i < 2 else 12 if i < 4 else 14), column=(0 if i % 2 == 0 else 1), padx=20, pady=5, sticky="w")

# Pre-fill customer details if user is a customer
if is_customer:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.first_name, u.last_name, u.email, c.phone, c.driving_license_number, c.customer_id
            FROM users u JOIN customers c ON c.user_id = u.user_id
            WHERE u.email = %s
        """, (user_email,))
        customer_data = cursor.fetchone()
        if customer_data:
            for i, label in enumerate(labels):
                value = customer_data[i] if i < 5 else ""
                entries[label].insert(0, str(value) if value is not None else "")
        else:
            messagebox.showerror("Error", "Customer data not found for this email")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch customer details: {e}")

form_frame.update()
form_frame.update_idletasks()
entries["First Name"].focus_set()  # Set focus to the first customer field

# Function to update vehicle and cost details
def update_vehicle_details(*args):
    selected_vehicle = vehicles_dropdown.get()
    if selected_vehicle in vehicle_dict:
        vehicle = vehicle_dict[selected_vehicle]
        year = vehicle[2]
        cost_per_day = vehicle[3]
        make = vehicle[4]
        model = vehicle[5]

        make_label.configure(text=f"Make: {make}")
        model_label.configure(text=f"Model: {model}")
        year_label.configure(text=f"Year: {year}")
        cost_per_day_value.configure(text=f"${cost_per_day:.2f}")

        total_cost_value.configure(text="$0.00")
        taxes_value.configure(text="$0.00")
        if not is_customer:
            discount_value.configure(text="$0.00")
        final_total_value.configure(text="$0.00")

        # Calculate costs only if both dates are provided and valid
        start_date_str = start_date_entry.get()
        end_date_str = end_date_entry.get()

        if start_date_str and end_date_str:  # Only proceed if both dates are filled
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                if end_date < start_date:
                    raise ValueError("End date cannot be before start date")
                if start_date < datetime.now().date():
                    raise ValueError("Start date cannot be in the past")
                days = (end_date - start_date).days + 1
                if days <= 0:
                    raise ValueError("Booking must be for at least 1 day")

                total_cost = cost_per_day * days
                # Apply discount (0% for customers, selected value for admin/staff)
                discount_percentage = float(discount_var.get().replace('%', '')) / 100 if not is_customer else 0.0
                discount = total_cost * discount_percentage
                discounted_cost = total_cost - discount
                taxes = discounted_cost * 0.06
                final_total = discounted_cost + taxes

                total_cost_value.configure(text=f"${total_cost:.2f}")
                taxes_value.configure(text=f"${taxes:.2f}")
                if not is_customer:
                    discount_value.configure(text=f"${discount:.2f}")
                final_total_value.configure(text=f"${final_total:.2f}")
            except ValueError as e:
                if "does not match format" in str(e):
                    return
                messagebox.showerror("Error", str(e))
    else:
        # Reset all fields if no valid vehicle is selected
        make_label.configure(text="Make: ")
        model_label.configure(text="Model: ")
        year_label.configure(text="Year: ")
        cost_per_day_value.configure(text="$0.00")
        total_cost_value.configure(text="$0.00")
        taxes_value.configure(text="$0.00")
        if not is_customer:
            discount_value.configure(text="$0.00")
        final_total_value.configure(text="$0.00")

# Bind the dropdown to update details
vehicles_dropdown.bind("<<ComboboxSelected>>", lambda event: update_vehicle_details())

book_vehicle_window.update()
update_vehicle_details()

# Confirm Booking button
def confirm_booking():
    try:
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        selected_vehicle = vehicles_dropdown.get()
        first_name = entries["First Name"].get().strip()
        last_name = entries["Last Name"].get().strip()
        email = entries["Email"].get().strip()
        phone = entries["Phone Number"].get().strip()
        driving_license = entries["Driving License Number"].get().strip()

        # Validation
        if not all([start_date, end_date, selected_vehicle, first_name, last_name, email, phone, driving_license]):
            messagebox.showerror("Error", "All fields must be filled")
            return
        if selected_vehicle not in vehicle_dict:
            messagebox.showerror("Error", "Please select a valid vehicle")
            return
        if len(driving_license) < 8:
            messagebox.showerror("Error", "Driving license number must be at least 8 characters")
            return

        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
        if end_date_dt < start_date_dt:
            messagebox.showerror("Error", "End date cannot be before start date")
            return
        if start_date_dt < datetime.now().date():
            messagebox.showerror("Error", "Start date cannot be in the past")
            return
        days = (end_date_dt - start_date_dt).days + 1
        if days <= 0:
            messagebox.showerror("Error", "Booking must be for at least 1 day")
            return

        vehicle = vehicle_dict[selected_vehicle]
        vehicle_id = vehicle[0]
        cost_per_day = vehicle[3]  # Already converted to float
        total_cost = cost_per_day * days
        discount_percentage = float(discount_var.get().replace('%', '')) / 100 if not is_customer else 0.0
        discount = total_cost * discount_percentage
        discounted_cost = total_cost - discount
        taxes = discounted_cost * 0.06  # Taxes on discounted amount
        total = discounted_cost + taxes

        # Check for overlapping rentals
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM rentals
            WHERE vehicle_id = %s AND status = 'active'
            AND (
                (start_date <= %s AND end_date >= %s)
                OR (start_date <= %s AND end_date >= %s)
                OR (start_date >= %s AND end_date <= %s)
            )
        """, (vehicle_id, start_date, start_date, end_date, end_date, start_date, end_date))
        result = cursor.fetchone()
        if cursor.description is None:
            raise Exception("Query execution failed: No result set returned")
        if result is None:
            print("No rows returned from overlapping check")
        elif result[0] > 0:
            messagebox.showerror("Error", "Vehicle is not available for the selected dates")
            cursor.close()
            return

        # Get or create customer
        if is_customer:
            cursor.execute(
                "SELECT c.customer_id, u.user_id FROM customers c JOIN users u ON c.user_id = u.user_id WHERE u.email = %s",
                (user_email,)
            )
            customer = cursor.fetchone()
            if customer is None:
                messagebox.showerror("Error", "Customer not found for this email")
                cursor.close()
                return
            customer_id, user_id = customer
            # Update users table
            cursor.execute(
                "UPDATE users SET first_name = %s, last_name = %s, email = %s WHERE user_id = %s",
                (first_name, last_name, email, user_id)
            )
            # Update customers table
            cursor.execute(
                "UPDATE customers SET phone = %s, driving_license_number = %s WHERE customer_id = %s",
                (phone, driving_license, customer_id)
            )
        else:
            # For admin/staff: Check if customer exists by email
            cursor.execute("SELECT c.customer_id, u.user_id FROM customers c JOIN users u ON c.user_id = u.user_id WHERE u.email = %s", (email,))
            customer = cursor.fetchone()
            if customer:
                # Customer exists, use existing customer_id
                customer_id, user_id = customer
                # Update existing customer details
                cursor.execute(
                    "UPDATE users SET first_name = %s, last_name = %s WHERE user_id = %s",
                    (first_name, last_name, user_id)
                )
                cursor.execute(
                    "UPDATE customers SET phone = %s, driving_license_number = %s WHERE customer_id = %s",
                    (phone, driving_license, customer_id)
                )
            else:
                # Create new customer
                cursor.execute(
                    "INSERT INTO users (first_name, last_name, email, password, role_id, status) VALUES (%s, %s, %s, %s, 3, 'active')",
                    (first_name, last_name, email, "default_password")  # Placeholder password
                )
                user_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO customers (user_id, phone, address1, city, zipcode, state, driving_license_number) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_id, phone, "Unknown", "Unknown", "00000", "Unknown", driving_license)  # Placeholder address
                )
                customer_id = cursor.lastrowid

        # Insert rental into database
        cursor.execute("""
            INSERT INTO rentals (customer_id, vehicle_id, start_date, end_date, total_cost, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (customer_id, vehicle_id, start_date, end_date, total, "active"))

        # Update vehicle status
        cursor.execute("UPDATE vehicles SET status = 'rented' WHERE vehicle_id = %s", (vehicle_id,))

        conn.commit()
        messagebox.showinfo("Success", "Booking confirmed successfully")
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), dashboard_script), user_email])
        book_vehicle_window.destroy()
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            messagebox.showerror("Error", f"Booking failed: {str(e)}")
        if 'cursor' in locals():
            if cursor.description is not None:
                cursor.fetchall()
            cursor.close()
        if 'conn' in locals():
            conn.close()

confirm_button = ctk.CTkButton(form_frame, text="Confirm Booking", font=("Arial", 16, "bold"), fg_color="yellow", text_color="black", width=300, height=50, command=confirm_booking)
confirm_button.grid(row=20, column=0, padx=20, pady=20, sticky="w")

book_vehicle_window.mainloop()