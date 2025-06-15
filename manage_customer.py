# manage_customer.py
import sys
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection
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
manage_customer_window = ctk.CTk()
manage_customer_window.title("Manage Customers - QuickDrive Rentals")
manage_customer_window.geometry("1100x600")
manage_customer_window.resizable(False, False)
manage_customer_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(manage_customer_window, fg_color=COLORS['color_1'], width=250, height=600)
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
home_label = ctk.CTkLabel(sidebar_frame, text="Home", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['home'], compound="left", anchor="w", cursor="hand2")
home_label.pack(pady=10, padx=10, fill="x")
home_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "staff_dashboard.py") if role_id == 2 else "admin_dashboard.py", user_email]) and manage_customer_window.destroy())

# Vehicle Management
vehicle_label = ctk.CTkLabel(sidebar_frame, text="Vehicle Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['vehicle'], compound="left", anchor="w", cursor="hand2")
vehicle_label.pack(pady=10, padx=10, fill="x")
vehicle_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_vehicle.py"), user_email]) and manage_customer_window.destroy())

# Customer Management
customer_label = ctk.CTkLabel(sidebar_frame, text="Customer Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['customer'], compound="left", anchor="w", fg_color="#FFA500", width=200)
customer_label.pack(pady=10, padx=10, fill="x")

# Rental History
history_label = ctk.CTkLabel(sidebar_frame, text="Bookings/Invoices", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['invoice'], compound="left", anchor="w", cursor="hand2")
history_label.pack(pady=10, padx=10, fill="x")
history_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "rental_history.py"), user_email]) and manage_customer_window.destroy())

# Reports
reports_label = ctk.CTkLabel(sidebar_frame, text="Reports", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['reports'], compound="left", anchor="w", cursor="hand2")
reports_label.pack(pady=10, padx=10, fill="x")
reports_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "reports.py"), user_email]) and manage_customer_window.destroy())

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")]) and manage_customer_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(manage_customer_window, fg_color=COLORS['white'], width=800, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)

# Manage Customers title
manage_customer_title = ctk.CTkLabel(main_frame, text="Manage Customers", font=("Arial", 24, "bold"), text_color="black")
manage_customer_title.place(x=20, y=20)

# Table frame
table_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['white'], width=680, height=500, border_width=2, border_color="black")
table_frame.pack_propagate(False)
table_frame.place(x=20, y=60)

# Create a canvas and scrollbar
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
headers = ["Customer ID", "First Name", "Last Name", "Email", "Phone", "Status"]
for col, header in enumerate(headers):
    header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), text_color="black", fg_color=COLORS['color_2'], width=100)
    header_label.grid(row=0, column=col, padx=1, pady=5)
action_header = ctk.CTkLabel(table_frame, text="Actions", font=("Arial", 14, "bold"), text_color="black", fg_color=COLORS['color_2'], width=120)
action_header.grid(row=0, column=len(headers), padx=1, pady=5)

# Function to validate email format
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Function to validate phone format
def validate_phone(phone):
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    return re.match(pattern, phone) is not None

# Function to open edit window
def edit_customer(customer_data):
    edit_window = ctk.CTkToplevel(manage_customer_window)
    edit_window.title("Edit Customer")
    edit_window.geometry("500x650")
    edit_window.resizable(False, False)
    edit_window.transient(manage_customer_window)
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
    labels = ["First Name", "Last Name", "Email", "Phone", "Address 1", "Address 2", "City", "Zipcode", "State", "Status"]
    entries = {}
    for i, label in enumerate(labels):
        ctk.CTkLabel(form_frame, text=label, font=("Arial", 14, "bold")).grid(row=i, column=0, padx=20,
                                                                              pady=(20 if i == 0 else 5), sticky="w")
        if label == "Status":
            entries[label] = ctk.CTkOptionMenu(form_frame, values=["active", "inactive"], width=300, height=40,
                                               font=("Arial", 14))
        else:
            entries[label] = ctk.CTkEntry(form_frame, width=300, height=40, font=("Arial", 14))
        entries[label].grid(row=i, column=1, padx=20, pady=(20 if i == 0 else 5), sticky="w")

    # Populate fields with current data
    entries["First Name"].insert(0, customer_data[1])
    entries["Last Name"].insert(0, customer_data[2])
    entries["Email"].insert(0, customer_data[3])
    entries["Phone"].insert(0, customer_data[4])
    entries["Address 1"].insert(0, customer_data[5])
    entries["Address 2"].insert(0, customer_data[6] if customer_data[6] else "")
    entries["City"].insert(0, customer_data[7])
    entries["Zipcode"].insert(0, customer_data[8])
    entries["State"].insert(0, customer_data[9])
    entries["Status"].set(customer_data[10])

    # Save button
    def save_changes():
        customer_id = customer_data[0]
        first_name = entries["First Name"].get().strip()
        last_name = entries["Last Name"].get().strip()
        email = entries["Email"].get().strip()
        phone = entries["Phone"].get().strip()
        address1 = entries["Address 1"].get().strip()
        address2 = entries["Address 2"].get().strip()
        city = entries["City"].get().strip()
        zipcode = entries["Zipcode"].get().strip()
        state = entries["State"].get().strip()
        status = entries["Status"].get()

        # Validation
        if not all([first_name, last_name, email, phone, address1, city, zipcode, state]):
            messagebox.showerror("Error", "All required fields must be filled")
            return
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        if not validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone format (e.g., 123-456-7890)")
            return
        if not (5 <= len(zipcode) <= 10 and zipcode.isalnum()):
            messagebox.showerror("Error", "Zipcode must be 5-10 alphanumeric characters")
            return

        # Check if email is unique
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s AND user_id != (SELECT user_id FROM customers WHERE customer_id = %s)", (email, customer_id))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Email already exists")
                return

            # Update users table
            cursor.execute(
                "UPDATE users SET first_name = %s, last_name = %s, email = %s, status = %s WHERE user_id = (SELECT user_id FROM customers WHERE customer_id = %s)",
                (first_name, last_name, email, status, customer_id)
            )
            # Update customers table
            cursor.execute(
                "UPDATE customers SET phone = %s, address1 = %s, address2 = %s, city = %s, zipcode = %s, state = %s WHERE customer_id = %s",
                (phone, address1, address2 if address2 else None, city, zipcode, state, customer_id)
            )
            conn.commit()
            messagebox.showinfo("Success", "Customer updated successfully")
            edit_window.destroy()
            # Refresh the customer list
            subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_customer.py"), user_email])
            manage_customer_window.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to update customer: {e}")
        finally:
            cursor.close()
            conn.close()

    save_button = ctk.CTkButton(edit_window, text="Save Changes", font=("Arial", 16, "bold"), fg_color=COLORS['color_1'], text_color="white", width=300, height=50, command=save_changes)
    save_button.place(x=130, y=550)

    form_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function to toggle customer status (active/inactive)
def toggle_status(customer_id, current_status):
    new_status = "inactive" if current_status == "active" else "active"
    if not messagebox.askyesno("Confirm", f"Are you sure you want to set this customer to '{new_status}'?"):
        return
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = %s WHERE user_id = (SELECT user_id FROM customers WHERE customer_id = %s)", (new_status, customer_id))
        conn.commit()
        messagebox.showinfo("Success", f"Customer status set to '{new_status}' successfully")
        # Refresh the customer list
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_customer.py"), user_email])
        manage_customer_window.destroy()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to update customer status: {e}")
    finally:
        cursor.close()
        conn.close()

# Fetch and display customers
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT c.customer_id, u.first_name, u.last_name, u.email, c.phone, c.address1, c.address2, c.city, c.zipcode, c.state, u.status
        FROM customers c
        JOIN users u ON c.user_id = u.user_id
        WHERE u.role_id = 3  -- Only fetch customers (role_id 3)
    """
    cursor.execute(query)
    customers = cursor.fetchall()

    display_indices = [0, 1, 2, 3, 4, 10]
    for row, customer in enumerate(customers, start=1):
        for col, idx in enumerate(display_indices):
            cell_label = ctk.CTkLabel(table_frame, text=str(customer[idx]) if customer[idx] else "", font=("Arial", 12), text_color="black", width=100)
            cell_label.grid(row=row, column=col, padx=1, pady=2)
        # Action buttons
        action_frame = ctk.CTkFrame(table_frame, fg_color=COLORS['white'])
        action_frame.grid(row=row, column=len(display_indices), padx=5, pady=2)
        edit_button = ctk.CTkButton(action_frame, text="Edit", font=("Arial", 12, "bold"), fg_color="blue", text_color="white", width=50, height=30, command=lambda c=customer: edit_customer(c))
        edit_button.pack(side="left", padx=2)
        # Inactive/Activate button based on current status
        status = customer[10]
        button_text = "Inactive" if status == "active" else "Activate"
        button_color = "red" if status == "active" else "green"
        status_button = ctk.CTkButton(action_frame, text=button_text, font=("Arial", 12, "bold"), fg_color=button_color,
                                      text_color="white", width=50, height=30,
                                      command=lambda c_id=customer[0], s=status: toggle_status(c_id, s))
        status_button.pack(side="left", padx=2)

        # Update the canvas scroll region for the table
    table_inner_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

except Exception as e:
    messagebox.showerror("Error", f"Failed to fetch customers: {e}")
    manage_customer_window.destroy()
    sys.exit(1)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

manage_customer_window.mainloop()