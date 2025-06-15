# reports.py
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection
from constants import COLORS
import subprocess
import sys
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image as PILImage
import io
import webbrowser
from tkcalendar import Calendar

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

user_email = sys.argv[1] if len(sys.argv) > 1 else "admin@example.com"


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
reports_window = ctk.CTk()
reports_window.title("Reports - QuickDrive Rentals")
reports_window.geometry("1100x600")
reports_window.resizable(False, False)
reports_window.configure(fg_color=COLORS['white'])

# Sidebar
sidebar_frame = ctk.CTkFrame(reports_window, fg_color=COLORS['color_1'], width=250, height=600)
sidebar_frame.pack_propagate(False)
sidebar_frame.place(x=0, y=0)

# Sidebar navigation options
nav_icons = {
    "home": ctk.CTkImage(light_image=PILImage.open("images/home_icon.png"), size=(50, 50)),
    "vehicle": ctk.CTkImage(light_image=PILImage.open("images/vehicle_icon.png"), size=(50, 50)),
    "customer": ctk.CTkImage(light_image=PILImage.open("images/customer_icon.png"), size=(50, 50)),
    "invoice": ctk.CTkImage(light_image=PILImage.open("images/invoice.png"), size=(50, 50)),
    "reports": ctk.CTkImage(light_image=PILImage.open("images/reports_icon.png"), size=(50, 50)),
    "logout": ctk.CTkImage(light_image=PILImage.open("images/logout_icon.png"), size=(50, 50))
}

# Home
dashboard_script = "staff_dashboard.py" if role_id == 2 else "admin_dashboard.py"
home_label = ctk.CTkLabel(sidebar_frame, text="Home", font=("Arial", 16, "bold"), text_color="black",
                          image=nav_icons['home'], compound="left", anchor="w", cursor="hand2")
home_label.pack(pady=10, padx=10, fill="x")
home_label.bind("<Button-1>", lambda event: subprocess.Popen(
    [sys.executable, os.path.join(os.getcwd(), dashboard_script), user_email]) and reports_window.destroy())

# Vehicle Management
vehicle_label = ctk.CTkLabel(sidebar_frame, text="Vehicle Management", font=("Arial", 16, "bold"), text_color="black",
                             image=nav_icons['vehicle'], compound="left", anchor="w", cursor="hand2")
vehicle_label.pack(pady=10, padx=10, fill="x")
vehicle_label.bind("<Button-1>", lambda event: subprocess.Popen(
    [sys.executable, os.path.join(os.getcwd(), "manage_vehicle.py"), user_email]) and reports_window.destroy())

# Customer Management
customer_label = ctk.CTkLabel(sidebar_frame, text="Customer Management", font=("Arial", 16, "bold"), text_color="black",
                              image=nav_icons['customer'], compound="left", anchor="w", cursor="hand2")
customer_label.pack(pady=10, padx=10, fill="x")
customer_label.bind("<Button-1>", lambda event: subprocess.Popen(
    [sys.executable, os.path.join(os.getcwd(), "manage_customer.py"), user_email]) and reports_window.destroy())

# Rental History
history_label = ctk.CTkLabel(sidebar_frame, text="Bookings/Invoices", font=("Arial", 16, "bold"), text_color="black",
                             image=nav_icons['invoice'], compound="left", anchor="w", cursor="hand2")
history_label.pack(pady=10, padx=10, fill="x")
history_label.bind("<Button-1>", lambda event: subprocess.Popen(
    [sys.executable, os.path.join(os.getcwd(), "rental_history.py"), user_email]) and reports_window.destroy())

# Reports
reports_label = ctk.CTkLabel(sidebar_frame, text="Reports", font=("Arial", 16, "bold"), text_color="black",
                             image=nav_icons['reports'], compound="left", anchor="w", fg_color="#FFA500", width=200)
reports_label.pack(pady=10, padx=10, fill="x")

# Log Out
logout_label = ctk.CTkLabel(sidebar_frame, text="Log Out", font=("Arial", 16, "bold"), text_color="black",
                            image=nav_icons['logout'], compound="left", anchor="w", cursor="hand2")
logout_label.pack(pady=10, padx=10, fill="x", side="bottom")
logout_label.bind("<Button-1>", lambda event: subprocess.Popen(
    [sys.executable, os.path.join(os.getcwd(), "login.py")]) and reports_window.destroy())

# Main content area
main_frame = ctk.CTkFrame(reports_window, fg_color=COLORS['white'], width=850, height=600)
main_frame.pack_propagate(False)
main_frame.place(x=250, y=0)

# Reports title
reports_title = ctk.CTkLabel(main_frame, text="Reports", font=("Arial", 24, "bold"), text_color="black")
reports_title.place(x=20, y=20)

# Report selection frame
report_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['white'], width=810, height=500)
report_frame.pack_propagate(False)
report_frame.place(x=20, y=60)

# Report type dropdown
report_type_label = ctk.CTkLabel(report_frame, text="Report Type:", font=("Arial", 16, "bold"), text_color="black")
report_type_label.place(x=20, y=20)
report_types = ["Revenue Report", "Vehicle Utilization Report", "Customer Activity Report", "Rental Status Report"]
report_type_var = tk.StringVar(value=report_types[0])
report_type_dropdown = ctk.CTkOptionMenu(report_frame, values=report_types, variable=report_type_var,
                                         font=("Arial", 16), fg_color=COLORS['color_2'], text_color="black", width=300,
                                         height=40)
report_type_dropdown.place(x=200, y=20)


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

    def on_focus_out(event):
        # Close the calendar if focus is lost
        if not top.focus_get():
            top.destroy()

    # Create the popup window
    top = tk.Toplevel(reports_window)
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
    cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 10), background="white",
                   foreground="black")
    cal.pack(pady=5)

    # Add the Select button
    select_button = ctk.CTkButton(top, text="Select", command=set_date, font=("Arial", 14), fg_color="green",
                                  text_color="white", width=100, height=30)
    select_button.pack(pady=5)

    # Bind focus out event to close the popup
    top.bind("<FocusOut>", on_focus_out)

    # Ensure the popup stays on top and grabs focus
    top.transient(reports_window)
    top.grab_set()
    top.focus_set()


# From Date field with calendar button
from_date_label = ctk.CTkLabel(report_frame, text="From Date:", font=("Arial", 16, "bold"), text_color="black")
from_date_label.place(x=20, y=80)
from_date_entry = ctk.CTkEntry(report_frame, font=("Arial", 16), width=300, height=40,
                               placeholder_text="e.g., 2025-01-01")
from_date_entry.place(x=200, y=80)
from_date_button = ctk.CTkButton(report_frame, text="📅", font=("Arial", 14), width=40, height=40, fg_color="darkblue",
                                 text_color="white", command=lambda: open_calendar(from_date_entry, from_date_button))
from_date_button.place(x=510, y=80)

# To Date field with calendar button
to_date_label = ctk.CTkLabel(report_frame, text="To Date:", font=("Arial", 16, "bold"), text_color="black")
to_date_label.place(x=20, y=140)
to_date_entry = ctk.CTkEntry(report_frame, font=("Arial", 16), width=300, height=40,
                             placeholder_text="e.g., 2025-12-31")
to_date_entry.place(x=200, y=140)
to_date_button = ctk.CTkButton(report_frame, text="📅", font=("Arial", 14), width=40, height=40, fg_color="darkblue",
                               text_color="white", command=lambda: open_calendar(to_date_entry, to_date_button))
to_date_button.place(x=510, y=140)


# Function to validate date format
def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# Function to add header and footer to the PDF
def add_header_footer(canvas, doc):
    # Header
    canvas.saveState()
    try:
        canvas.drawImage("images/loginLogo.jpg", 50, letter[1] - 80, width=100, height=50)
    except Exception:
        canvas.setFont("Helvetica", 10)
        canvas.drawString(50, letter[1] - 60, "[Logo Placeholder]")

    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawCentredString(letter[0] / 2, letter[1] - 50, "QuickDrive Rentals")
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(letter[0] / 2, letter[1] - 70, "booking@quickdrive.com")
    canvas.drawCentredString(letter[0] / 2, letter[1] - 85, "222 555 7777")

    # Footer
    canvas.setFont("Helvetica", 8)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S PDT")
    canvas.drawCentredString(letter[0] / 2, 50, f"Generated on: {timestamp}")
    canvas.restoreState()


# Function to generate Revenue Report
def generate_revenue_report(from_date, to_date, story, temp_files):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT DATE_FORMAT(r.start_date, '%Y-%m') AS period, SUM(r.total_cost) AS revenue
        FROM rentals r
        WHERE r.status = 'completed' AND r.start_date BETWEEN %s AND %s
        GROUP BY DATE_FORMAT(r.start_date, '%Y-%m')
        ORDER BY period
    """
    cursor.execute(query, (from_date, to_date))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Prepare table data
    table_data = [["Period", "Revenue (USD)"]]
    periods = []
    revenues = []
    for row in data:
        table_data.append([row[0], f"{float(row[1]):.2f}"])
        periods.append(row[0])
        revenues.append(float(row[1]))

    # Create table
    table = Table(table_data, colWidths=[150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5 * inch))

    # Create line chart
    plt.figure(figsize=(8, 4))
    plt.plot(periods, revenues, marker='o')
    plt.title("Revenue Trend")
    plt.xlabel("Period (YYYY-MM)")
    plt.ylabel("Revenue (USD)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save chart to a temporary file
    chart_filename = "revenue_chart.png"
    plt.savefig(chart_filename, format='png')
    plt.close()
    temp_files.append(chart_filename)  # Add to list for cleanup later

    # Embed chart in PDF
    img = Image(chart_filename, width=400, height=200)
    story.append(img)


# Function to generate Vehicle Utilization Report
def generate_vehicle_utilization_report(from_date, to_date, story, temp_files):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all vehicles
    cursor.execute("SELECT vehicle_id, CONCAT(make, ' ', model) AS vehicle_name FROM vehicles")
    vehicles = cursor.fetchall()

    # Calculate total days in the date range
    start_dt = datetime.strptime(from_date, "%Y-%m-%d")
    end_dt = datetime.strptime(to_date, "%Y-%m-%d")
    total_days = (end_dt - start_dt).days + 1

    # Calculate utilization for each vehicle
    table_data = [["Vehicle", "Utilization (%)"]]
    vehicle_names = []
    utilizations = []
    for vehicle in vehicles:
        vehicle_id = vehicle[0]
        vehicle_name = vehicle[1]
        # Calculate the total rented days within the date range
        query = """
            SELECT SUM(
                DATEDIFF(
                    LEAST(r.end_date, %s),
                    GREATEST(r.start_date, %s)
                ) + 1
            ) AS rented_days
            FROM rentals r
            WHERE r.vehicle_id = %s
            AND r.start_date <= %s
            AND r.end_date >= %s
            AND r.status = 'active'
        """
        cursor.execute(query, (to_date, from_date, vehicle_id, to_date, from_date))
        result = cursor.fetchone()
        rented_days = result[0] if result[0] is not None else 0
        # Ensure rented_days is not negative or greater than total_days
        rented_days = max(0, min(rented_days, total_days))
        # Calculate utilization as a percentage
        utilization = (rented_days / total_days) * 100 if total_days > 0 else 0
        table_data.append([vehicle_name, f"{utilization:.2f}%"])
        vehicle_names.append(vehicle_name)
        utilizations.append(utilization)

    cursor.close()
    conn.close()

    # Create table
    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5 * inch))

    # Create bar chart
    plt.figure(figsize=(8, 4))
    bars = plt.bar(vehicle_names, utilizations, color='skyblue')
    plt.title("Vehicle Utilization")
    plt.xlabel("Vehicle")
    plt.ylabel("Utilization (%)")
    plt.ylim(0, 100)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()

    # Add percentage labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom', fontsize=8)

    # Save chart to a temporary file
    chart_filename = "vehicle_utilization_chart.png"
    plt.savefig(chart_filename, format='png')
    plt.close()
    temp_files.append(chart_filename)  # Add to list for cleanup later

    # Embed chart in PDF
    img = Image(chart_filename, width=400, height=200)
    story.append(img)


# Function to generate Customer Activity Report
def generate_customer_activity_report(from_date, to_date, story, temp_files):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT CONCAT(u.first_name, ' ', u.last_name) AS customer_name, COUNT(r.rental_id) AS rental_count
        FROM rentals r
        JOIN customers c ON r.customer_id = c.customer_id
        JOIN users u ON c.user_id = u.user_id
        WHERE r.start_date BETWEEN %s AND %s
        GROUP BY r.customer_id, customer_name
        ORDER BY rental_count DESC
    """
    cursor.execute(query, (from_date, to_date))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Prepare table data
    table_data = [["Customer", "Number of Rentals"]]
    customer_names = []
    rental_counts = []
    for row in data:
        table_data.append([row[0], str(row[1])])
        customer_names.append(row[0])
        rental_counts.append(row[1])

    # Create table
    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5 * inch))

    # Create bar chart
    plt.figure(figsize=(8, 4))
    bars = plt.bar(customer_names, rental_counts, color='lightcoral')
    plt.title("Customer Activity Distribution")
    plt.xlabel("Customer")
    plt.ylabel("Number of Rentals")
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()

    # Add count labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{int(yval)}', ha='center', va='bottom', fontsize=8)

    # Save chart to a temporary file
    chart_filename = "customer_activity_chart.png"
    plt.savefig(chart_filename, format='png')
    plt.close()
    temp_files.append(chart_filename)  # Add to list for cleanup later

    # Embed chart in PDF
    img = Image(chart_filename, width=400, height=200)
    story.append(img)


# Function to generate Rental Status Report
def generate_rental_status_report(from_date, to_date, story, temp_files):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT r.status, COUNT(r.rental_id) AS count
        FROM rentals r
        WHERE r.start_date BETWEEN %s AND %s
        GROUP BY r.status
    """
    cursor.execute(query, (from_date, to_date))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Prepare table data
    table_data = [["Status", "Count"]]
    statuses = []
    counts = []
    for row in data:
        table_data.append([row[0], str(row[1])])
        statuses.append(row[0])
        counts.append(row[1])

    # Create table
    table = Table(table_data, colWidths=[150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5 * inch))

    # Create pie chart
    plt.figure(figsize=(8, 4))
    plt.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=140)
    plt.title("Rental Status Distribution")
    plt.tight_layout()

    # Save chart to a temporary file
    chart_filename = "rental_status_chart.png"
    plt.savefig(chart_filename, format='png')
    plt.close()
    temp_files.append(chart_filename)  # Add to list for cleanup later

    # Embed chart in PDF
    img = Image(chart_filename, width=400, height=200)
    story.append(img)


# Function to generate the report
def generate_report():
    report_type = report_type_var.get()
    from_date = from_date_entry.get()
    to_date = to_date_entry.get()

    # Validate dates
    if not from_date or not to_date:
        messagebox.showerror("Error", "Please select both From Date and To Date.")
        return
    if not validate_date(from_date) or not validate_date(to_date):
        messagebox.showerror("Error", "Dates must be in YYYY-MM-DD format.")
        return
    if datetime.strptime(from_date, "%Y-%m-%d") > datetime.strptime(to_date, "%Y-%m-%d"):
        messagebox.showerror("Error", "From Date must be before To Date.")
        return

    # List to keep track of temporary files
    temp_files = []

    # Generate PDF using SimpleDocTemplate
    filename = f"{report_type.replace(' ', '_').lower()}_{from_date}_to_{to_date}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=100)

    # Build the story
    story = []
    styles = getSampleStyleSheet()

    # Add title and date range
    story.append(Paragraph(f"<b>{report_type}</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Date Range: {from_date} to {to_date}", styles['Normal']))
    story.append(Spacer(1, 0.5 * inch))

    # Generate report based on type
    try:
        if report_type == "Revenue Report":
            generate_revenue_report(from_date, to_date, story, temp_files)
        elif report_type == "Vehicle Utilization Report":
            generate_vehicle_utilization_report(from_date, to_date, story, temp_files)
        elif report_type == "Customer Activity Report":
            generate_customer_activity_report(from_date, to_date, story, temp_files)
        elif report_type == "Rental Status Report":
            generate_rental_status_report(from_date, to_date, story, temp_files)

        # Build the PDF
        doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

        # Clean up temporary files after the PDF is built
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        # Open the PDF
        webbrowser.open(os.path.abspath(filename))
    except Exception as e:
        # Clean up temporary files in case of an error
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        messagebox.showerror("Error", f"Failed to generate report: {e}")


# Generate Report button
generate_button = ctk.CTkButton(report_frame, text="Generate Report", font=("Arial", 16, "bold"), fg_color="green",
                                text_color="white", width=300, height=50, command=generate_report)
generate_button.place(x=200, y=200)

reports_window.mainloop()