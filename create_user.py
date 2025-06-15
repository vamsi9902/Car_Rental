# create_user.py
import sys
import os
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection, generate_email_address, resize_image
from constants import COLORS, ROLES
import subprocess
import sys

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

admin_email = sys.argv[1] if len(sys.argv) > 1 else "admin@example.com"

create_user_window = ctk.CTk()
create_user_window.title("Create User - QuickDrive Rentals")
create_user_window.geometry("800x600")
create_user_window.resizable(False, False)
create_user_window.configure(fg_color=COLORS['color_1'])

# Create User Frame
left_frame = ctk.CTkFrame(create_user_window, fg_color=COLORS['color_2'], width=400, height=400)
left_frame.pack_propagate(False)
left_frame.place(x=50, y=100)

# Logo at the top-left
logo_image = resize_image((100, 50), 'images/loginLogo.jpg')
logo_label = ctk.CTkLabel(create_user_window, text="", image=logo_image)
logo_label.place(x=20, y=20)

# Logo Title
logotitle_label = ctk.CTkLabel(create_user_window, text="QuickDrive Rentals", font=("Aclonica", 16, "bold"), text_color="white")
logotitle_label.place(x=90, y=20)

# Form title
create_user_title = ctk.CTkLabel(left_frame, text="Create User", font=("Abril Fatface", 18, "bold"), text_color="black")
create_user_title.grid(row=0, column=0, columnspan=1, pady=10)

# Form fields
first_name_label = ctk.CTkLabel(left_frame, text="First Name", font=("Abril Fatface", 12, "bold"), text_color="black")
first_name_label.grid(row=1, column=0, padx=50, pady=5, sticky="w")
first_name_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="John")
first_name_entry.grid(row=2, column=0, padx=50, pady=5, sticky="w")

last_name_label = ctk.CTkLabel(left_frame, text="Last Name", font=("Abril Fatface", 12, "bold"), text_color="black")
last_name_label.grid(row=3, column=0, padx=50, pady=5, sticky="w")
last_name_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="Doe")
last_name_entry.grid(row=4, column=0, padx=50, pady=5, sticky="w")

role_label = ctk.CTkLabel(left_frame, text="Role", font=("Abril Fatface", 12, "bold"), text_color="black")
role_label.grid(row=5, column=0, padx=50, pady=5, sticky="w")
role_dropdown = ctk.CTkOptionMenu(left_frame, width=300, values=['admin', 'staff'])
role_dropdown.grid(row=6, column=0, padx=50, pady=5, sticky="w")

# Create button
create_button = ctk.CTkButton(left_frame, text="Create User", width=300, height=40, fg_color="#1B5671", text_color="white", font=("Arial", 16, "bold"), command=lambda: create_account())
create_button.grid(row=7, column=0, padx=50, pady=(30, 0), sticky="w")

# Back to dashboard link
back_label = ctk.CTkLabel(left_frame, text="Back to Dashboard", font=("Arial", 10, "bold"), text_color="black", cursor="hand2")
back_label.grid(row=8, column=0, padx=150, pady=0, sticky="w")
back_label.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "admin_dashboard.py"), admin_email]) and create_user_window.destroy())

# Right side - Car image banner
car_image = resize_image((600, 1200), 'images/loginBanner.jpg')
car_label = ctk.CTkLabel(create_user_window, text="", image=car_image)
car_label.place(x=500, y=0)

# Account creation
def create_account():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    role = role_dropdown.get()

    if not all([first_name, last_name, role]):
        messagebox.showerror("Error", "All fields are required")
        return

    # Generate email for staff/admin
    email = generate_email_address(first_name, last_name)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Email already in use")
            return

        # Insert into Users table
        cursor.execute("INSERT INTO users (first_name, last_name, email, password, role_id, status) VALUES (%s, %s, %s, %s, %s, %s)",
                       (first_name.lower(), last_name.lower(), email, 'password', ROLES.index(role) + 1, 'inactive'))
        conn.commit()
        messagebox.showinfo("Success", f"Account created successfully with email {email}. The user must log in and change their password.")
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "admin_dashboard.py"), admin_email])
        create_user_window.destroy()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to create account: {e}")
    finally:
        cursor.close()
        conn.close()

create_user_window.mainloop()