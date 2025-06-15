# QuickDrive Rentals - Car Rental Management System

## Overview
QuickDrive Rentals is a desktop application developed to streamline car rental operations for QuickDrive Rentals. Built with Python and MySQL, it provides a user-friendly interface using the `customtkinter` library. The system supports three user roles—Admins, Staff, and Customers—with tailored dashboards and functionalities to manage users, vehicles, bookings, rental history, and generate reports.

### Key Features
- **Admin Dashboard**: Full control over customers, vehicles, bookings, rental history, and report generation.
- **Staff Dashboard**: Manage customer and vehicle data, handle bookings, and view reports.
- **Customer Dashboard**: View and edit bookings, book vehicles, and access rental history.
- **Reports**: Generate PDF reports (Revenue, Vehicle Utilization, Customer Activity, Rental Status) with charts using `reportlab` and `matplotlib`.
- **Receipts**: Generate PDF receipts for past bookings with tax calculations.
- **Role-Based Access**: Secure login system with role-specific dashboards (Admins: role_id=1, Staff: role_id=2, Customers: role_id=3).
- **Navigation**: Intuitive sidebar navigation for all modules.

## System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Software**:
  - Python 3.8 or higher
  - MySQL Server
- **Python Libraries**:
  - `customtkinter` (for UI)
  - `mysql-connector-python` (for database connectivity)
  - `pillow` (for image processing)
  - `reportlab` (for PDF generation)
  - `matplotlib` (for chart generation in reports)
  - `tkcalendar` (for date selection)
- **Hardware**: Minimum 4GB RAM, 1GB free disk space
- **Other**: Default PDF viewer for viewing receipts and reports

## Installation
Follow these steps to set up the QuickDrive Rentals application locally:

1. **Set Up MySQL Database**:
   - Install MySQL Server from [mysql.com](https://www.mysql.com).
   - Create a database (e.g., `quickdrive_db`).
   - Set up the required tables: `users`, `customers`, `vehicles`, `rentals`. Refer to the project documentation or database schema for table structures.
   - Update `config.py` with your database credentials:
     ```python
     db_config = {
         'host': 'localhost',
         'user': 'your_username',
         'password': 'your_password',
         'database': 'quickdrive_db'
     }
     ```

2. **Install Python and Dependencies**:
   - Download and install Python 3.8+ from [python.org](https://www.python.org).
   - Install required Python libraries using pip:
     ```bash
     pip install customtkinter mysql-connector-python pillow reportlab matplotlib tkcalendar
     ```

3. **Download Project Files**:
   - Clone the repository or download the project files to a local directory.
   - Ensure all Python scripts (e.g., `home.py`, `login.py`, etc.) are in the project folder.

4. **Verify Setup**:
   - Confirm MySQL Server is running.
   - Verify database credentials in `config.py`.
   - Ensure all required libraries are installed by running:
     ```bash
     pip list
     ```

## Usage
### Launching the Application
1. Open a terminal or command prompt in the project directory.
2. Run the application:
   ```bash
   python home.py
   ```
3. The login screen (`login.py`) will appear.

### Logging In
1. On the login screen, enter your email and password.
2. (Optional) Check "Show Password" to view your password.
3. (Optional) Check "Remember me" to save credentials for future logins.
4. Click "Login" to access your dashboard:
   - Admins (role_id=1): Redirected to Admin Dashboard.
   - Staff (role_id=2): Redirected to Staff Dashboard.
   - Customers (role_id=3): Redirected to Customer Dashboard.
5. For new or inactive accounts, follow the prompt to change your password (see "Changing Password" below).

### Signing Up as a New Customer
1. On the login screen, click "Sign Up" to open the registration form.
2. Fill in the required fields:
   - **Email**: Must be unique and valid (e.g., `user@example.com`).
   - **First Name, Last Name**: Enter your full name.
   - **Phone**: 10-digit number (e.g., 999-999-9999).
   - **Address Line 1, Address Line 2 (optional)**: Enter your address.
   - **City, Zipcode (5-digit), State**: Select state from a dropdown.
3. Click "Submit" to create the account.
4. Log in with your email and the default password (provided by the system or admin).
5. On first login, you must change your password.

### Changing Password
1. If prompted (e.g., first login or inactive account), the password change window appears.
2. Enter a new password (minimum 8 characters).
3. Re-enter the password in the "Confirm Password" field.
4. (Optional) Check "Show Password" to verify input.
5. Click "Submit" to update the password and access your dashboard.

### Navigating the System
- The system uses a sidebar for navigation in all modules.
- Sidebar options include role-specific functionalities and a "Logout" button.
- Refer to the sections below for detailed instructions on each dashboard and functionality.

### Admin Dashboard
- **Purpose**: Provides full control over the system.
- **Features**:
  - Displays admin name and current date.
  - Quick statistics: Total Vehicles, Active Bookings, Revenue, Average Rate, Monthly Revenue.
  - Sidebar links: Manage Customers, Manage Vehicles, View Bookings, Rental History, Reports, Logout.
- **Navigation**: Use the sidebar to access all functionalities.

### Staff Dashboard
- **Purpose**: Supports staff in managing operations.
- **Features**:
  - Displays staff name and current date.
  - Quick statistics: Total Vehicles, Active Bookings, Revenue, Average Rate, Monthly Revenue.
  - Sidebar links: Manage Customers, Manage Vehicles, View Bookings, Rental History, Reports, Logout.
- **Navigation**: Similar to Admin Dashboard, with staff-specific permissions.

### Customer Dashboard
- **Purpose**: Allows customers to manage their bookings and view history.
- **Features**:
  - Displays customer name.
  - Sidebar links: View Bookings, Book a Vehicle, Rental History, Logout.
- **Navigation**: Use the sidebar to access customer functionalities.

## Core Functionalities
### 1. Managing Customers (Admin/Staff)
1. From the dashboard, click "Manage Customers" in the sidebar.
2. View a table with columns: ID, First Name, Last Name, Email, Phone, Status.
3. **Edit a Customer**:
   - Click "Edit" next to a customer.
   - Update fields (email, phone, address, etc.) in the form.
   - Click "Submit" to save changes.
4. **Toggle Status**:
   - Click "Toggle Status" to switch between Active and Inactive.
5. Click "Home" to return to the dashboard.

### 2. Managing Vehicles (Admin/Staff)
1. Click "Manage Vehicles" in the sidebar.
2. View a table with columns: ID, Year, License Plate, Cost Per Day, Status.
3. **Edit a Vehicle**:
   - Click "Edit" next to a vehicle.
   - Update fields (make, model, year, license plate, cost per day).
   - Click "Submit" to save changes.
4. **Toggle Status**:
   - Click "Toggle Status" to switch between Available and Unavailable.
5. Click "Home" to return to the dashboard.

### 3. Viewing and Editing Bookings
1. Click "View Bookings" in the sidebar.
2. View a table of active/upcoming bookings with columns: Rental ID, Customer Name, Vehicle, Start Date, End Date, Total Cost, Status.
   - Customers see only their bookings; admins/staff see all.
3. **Edit a Booking**:
   - Click "Edit" next to a booking.
   - Update start and end dates (and status, if admin/staff).
   - Click "Submit" to save; the total cost is recalculated.
4. **Cancel a Booking**:
   - Click "Cancel" to set the booking status to Cancelled and vehicle status to Available.
5. Click "Home" to return to the dashboard.

### 4. Viewing Rental History
1. Click "Rental History" in the sidebar.
2. View a table of past bookings with columns: Rental ID, Customer Name, Vehicle, Start Date, End Date, Total Cost, Status.
   - Customers see only their history; admins/staff see all.
3. **Generate a Receipt**:
   - Click "View Receipt" next to a booking.
   - A PDF receipt is generated with booking details, customer info, and tax calculations.
   - The PDF opens in your default PDF viewer.
4. Click "Home" to return to the dashboard.

### 5. Generating Reports (Admin/Staff)
1. Click "Reports" in the sidebar.
2. Select a report type from the dropdown:
   - Revenue Report
   - Vehicle Utilization Report
   - Customer Activity Report
   - Rental Status Report
3. Choose a date range using the calendar popups.
4. Click "Generate Report" to create a PDF with tables and charts (e.g., line, bar, or pie).
5. The PDF opens in your default PDF viewer.
6. Click "Home" to return to the dashboard.

### Logging Out
1. Click "Logout" in the sidebar from any module.
2. You will be redirected to the login screen (`login.py`).
3. Log in again or close the application.

## Folder Structure
```
quickdrive-rentals/
├── home.py                # Application entry point
├── login.py               # Login and signup interface
├── config.py              # Database configuration
├── admin_dashboard.py     # Admin dashboard module
├── staff_dashboard.py     # Staff dashboard module
├── customer_dashboard.py  # Customer dashboard module
├── manage_customers.py    # Customer management module
├── manage_vehicles.py     # Vehicle management module
├── view_bookings.py       # Booking management module
├── rental_history.py      # Rental history module
├── reports.py             # Report generation module
├── README.md              # This file
```

## Troubleshooting
- **Login Issues**:
  - Ensure email and password are correct.
  - Follow password change instructions (see "Changing Password") if prompted.
  - Contact your admin if the account is inactive.
- **Database Errors**:
  - Verify MySQL Server is running (`mysqladmin -u root -p status`).
  - Check `config.py` for correct database credentials.
- **PDF Generation Issues**:
  - Ensure a default PDF viewer is installed (e.g., Adobe Acrobat, SumatraPDF).
  - Verify sufficient disk space (minimum 1GB free).
- **Application Crashes**:
  - Confirm all required libraries are installed (`pip list`).
  - Restart the application with `python home.py`.
- **Additional Help**: Refer to Section 7 of the User Manual for detailed troubleshooting steps.

## Course Information
- **Course Number**: BIS698
- **Course Name**: Information Systems Project