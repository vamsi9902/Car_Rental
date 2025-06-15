# rental_history.py
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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import webbrowser

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
rental_history_window = ctk.CTk()
rental_history_window.title("Rental History - QuickDrive Rentals")
rental_history_window.geometry("1200x600")
rental_history_window.resizable(False, False)
rental_history_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(rental_history_window, fg_color=COLORS['color_1'], width=250, height=600)
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
home_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), dashboard_script), user_email]) and rental_history_window.destroy())

# Admin/Staff-specific sidebar options
if not is_customer:
    # Vehicle Management
    vehicle_label = ctk.CTkLabel(sidebar_frame, text="Vehicle Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['vehicle'], compound="left", anchor="w", cursor="hand2")
    vehicle_label.pack(pady=10, padx=10, fill="x")
    vehicle_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_vehicle.py"), user_email]) and rental_history_window.destroy())

    # Customer Management
    customer_label = ctk.CTkLabel(sidebar_frame, text="Customer Management", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['customer'], compound="left", anchor="w", cursor="hand2")
    customer_label.pack(pady=10, padx=10, fill="x")
    customer_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "manage_customer.py"), user_email]) and rental_history_window.destroy())

    # Rental History
    history_label = ctk.CTkLabel(sidebar_frame, text="Bookings/Invoices", font=("Arial", 16, "bold"),
                                 text_color="black", image=nav_icons['invoice'], compound="left", anchor="w", fg_color="#FFA500", width=200,
                                 cursor="hand2")
    history_label.pack(pady=10, padx=10, fill="x")
    history_label.bind("<Button-1>", lambda event: subprocess.Popen(
        [sys.executable, os.path.join(os.getcwd(), "rental_history.py"),
         user_email]) and rental_history_window.destroy())

    # Reports
    reports_label = ctk.CTkLabel(sidebar_frame, text="Reports", font=("Arial", 16, "bold"), text_color="black",
                                 image=nav_icons['reports'], compound="left", anchor="w", cursor="hand2")
    reports_label.pack(pady=10, padx=10, fill="x")
    reports_label.bind("<Button-1>", lambda event: subprocess.Popen(
        [sys.executable, os.path.join(os.getcwd(), "reports.py"), user_email]) and rental_history_window.destroy())

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black", image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "login.py")]) and rental_history_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(rental_history_window, fg_color=COLORS['white'], width=950, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)

# Rental History title
rental_history_title = ctk.CTkLabel(main_frame, text="Rental History", font=("Arial", 24, "bold"), text_color="black")
rental_history_title.place(x=20, y=20)

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
    header_label.grid(row=0, column=col, padx=5, pady=5)

# Add Actions header separately
action_header = ctk.CTkLabel(
    header_frame,
    text="Actions",
    font=("Arial", 14, "bold"),
    text_color="black",
    fg_color=COLORS['color_2'],
    width=120,
    anchor="center"
)
action_header.grid(row=0, column=len(headers), padx=3, pady=5)

# Function to fetch customer details
def fetch_customer_details(rental_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT u.email
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN users u ON c.user_id = u.user_id
            WHERE r.rental_id = %s
        """
        cursor.execute(query, (rental_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch customer details: {e}")
        return None

# Function to generate PDF receipt
def generate_receipt(booking_data):
    rental_id = booking_data[0]
    customer_name = booking_data[1]
    vehicle = booking_data[2]
    start_date = str(booking_data[3])
    end_date = str(booking_data[4])
    total_cost = float(booking_data[5])

    # Fetch customer details
    customer_email = fetch_customer_details(rental_id)
    if customer_email is None:
        customer_email = "Not available"

    filename = f"receipt_{rental_id}.pdf"
    c = Canvas(filename, pagesize=letter)
    width, height = letter

    # Draw logo
    try:
        c.drawImage("images/loginLogo.jpg", width - 570, height - 80, width=100, height=50)
    except Exception as e:
        c.setFont("Helvetica", 10)
        c.drawString(width - 150, height - 60, "[Logo Placeholder]")

    # Company details
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "QuickDrive Rentals")
    c.setFont("Helvetica", 10)
    c.drawString(250, height - 70, "booking@quickdrive.com")
    c.drawString(270, height - 85, "222 555 7777")

    # Receipt title and number
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120, f"Car Rental Receipt")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 135, f"Receipt Number: {rental_id}")

    # Customer details
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 160, f"Prepared for: {customer_name}")
    c.drawString(50, height - 175, f"Email: {customer_email}")

    # Date
    issuance_date = datetime.now().strftime("%B %d, %Y")
    c.drawString(50, height - 190, f"Date: {issuance_date}")

    # Calculate rental duration and cost per day
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end_dt - start_dt).days + 1
    cost_per_day = total_cost / days if days > 0 else total_cost

    # Calculate tax (6%)
    tax_rate = 0.06
    tax_amount = total_cost * tax_rate
    grand_total = total_cost + tax_amount

    # Charges table
    data = [
        ["Description", "Quantity", "Price", "Total"],
        [f"Car - {vehicle}", str(days), f"USD {cost_per_day:.2f} Unit", f"USD {total_cost:.2f}"],
        ["Tax", "6%", "", f"USD {tax_amount:.2f}"],
        ["TOTAL", "", "", f"USD {grand_total:.2f}"]
    ]
    table = Table(data, colWidths=[200, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 285)

    # Terms and Conditions
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 315, "Terms & Conditions")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 330, "• The above has been billed & delivered to the customer.")
    c.drawString(50, height - 345, "• The company has received the customer’s full payment.")

    # Draw timestamp at the bottom
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S PDT")
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 50, f"Generated on: {timestamp}")

    # Save the PDF and open it
    c.showPage()
    c.save()

    # Open the PDF with the default viewer
    try:
        webbrowser.open(os.path.abspath(filename))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open receipt: {e}")

# Fetch and display rental history
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
        # Fetch past bookings for this customer
        query = """
            SELECT r.rental_id, CONCAT(u.first_name, ' ', u.last_name) AS customer_name,
                   CONCAT(v.make, ' ', v.model, ' (', v.license_plate, ')') AS vehicle,
                   r.start_date, r.end_date, r.total_cost, r.status
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN users u ON c.user_id = u.user_id
            JOIN vehicles v ON r.vehicle_id = v.vehicle_id
            WHERE r.customer_id = %s AND (r.status IN ('completed', 'cancelled') OR r.end_date < CURDATE())
            ORDER BY r.start_date DESC
        """
        cursor.execute(query, (customer_id,))
    else:
        # Fetch all past bookings for admin/staff
        query = """
            SELECT r.rental_id, CONCAT(u.first_name, ' ', u.last_name) AS customer_name,
                   CONCAT(v.make, ' ', v.model, ' (', v.license_plate, ')') AS vehicle,
                   r.start_date, r.end_date, r.total_cost, r.status
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN users u ON c.user_id = u.user_id
            JOIN vehicles v ON r.vehicle_id = v.vehicle_id
            WHERE r.status IN ('completed', 'cancelled') OR r.end_date < CURDATE()
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
        # Action button: View Receipt
        action_frame = ctk.CTkFrame(table_inner_frame, fg_color=COLORS['white'])
        action_frame.grid(row=row, column=len(display_indices), padx=5, pady=2)
        receipt_button = ctk.CTkButton(action_frame, text="View Receipt", font=("Arial", 12, "bold"), fg_color="green", text_color="white", width=100, height=30, command=lambda b=booking: generate_receipt(b))
        receipt_button.pack(side="left", padx=2)

    # If no bookings, display a message
    if not bookings:
        no_bookings_label = ctk.CTkLabel(table_inner_frame, text="No past bookings found.", font=("Arial", 14), text_color="black")
        no_bookings_label.grid(row=1, column=0, columnspan=len(headers) + 1, pady=20)

    # Update the canvas scroll region
    table_inner_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

except Exception as e:
    messagebox.showerror("Error", f"Failed to fetch rental history: {e}")
    rental_history_window.destroy()
    sys.exit(1)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

rental_history_window.mainloop()