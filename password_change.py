# password_change.py
import sys
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils import get_db_connection, resize_image
from constants import COLORS
import subprocess
import sys

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

if len(sys.argv) < 3:
    email = "user@example.com"
    current_password = "passinit"
else:
    email = sys.argv[1]
    current_password = sys.argv[2]

password_change_window = ctk.CTk()
password_change_window.title("Change Password - QuickDrive Rentals")
password_change_window.geometry("800x600")
password_change_window.resizable(False, False)
password_change_window.configure(fg_color=COLORS['color_1'])

# Left frame for form
left_frame = ctk.CTkFrame(password_change_window, fg_color=COLORS['color_2'], width=400, height=500)
left_frame.pack_propagate(False)
left_frame.place(x=50, y=100)

# Logo at the top-left
logo_image = resize_image((100, 50), 'images/loginLogo.jpg')
logo_label = ctk.CTkLabel(password_change_window, text="", image=logo_image)
logo_label.place(x=20, y=20)

# Logo Title
logotitle_label = ctk.CTkLabel(password_change_window, text="QuickDrive Rentals", font=("Aclonica", 16, "bold"), text_color="white")
logotitle_label.place(x=90, y=20)

# Form title
change_password_title = ctk.CTkLabel(left_frame, text="Change Password", font=("Abril Fatface", 18, "bold"), text_color="black")
change_password_title.grid(row=0, column=0, columnspan=1, pady=10)

# Form fields
new_password_label = ctk.CTkLabel(left_frame, text="New Password", font=("Abril Fatface", 12, "bold"), text_color="black")
new_password_label.grid(row=1, column=0, padx=50, pady=5, sticky="w")
new_password_entry = ctk.CTkEntry(left_frame, show="*", width=300, height=35, border_color="black", border_width=1, placeholder_text="New Password")
new_password_entry.grid(row=2, column=0, padx=50, pady=5, sticky="w")

confirm_password_label = ctk.CTkLabel(left_frame, text="Confirm Password", font=("Abril Fatface", 12, "bold"), text_color="black")
confirm_password_label.grid(row=3, column=0, padx=50, pady=5, sticky="w")
confirm_password_entry = ctk.CTkEntry(left_frame, show="*", width=300, height=35, border_color="black", border_width=1, placeholder_text="Confirm Password")
confirm_password_entry.grid(row=4, column=0, padx=50, pady=5, sticky="w")

# Show Password checkbox
show_password_var = ctk.StringVar()
show_password_checkbox = ctk.CTkCheckBox(left_frame, text="Show Password", variable=show_password_var, onvalue="on", offvalue="off",
                                        command=lambda: [new_password_entry.configure(show="" if show_password_var.get() == "on" else "*"),
                                                        confirm_password_entry.configure(show="" if show_password_var.get() == "on" else "*")],
                                        text_color="black")
show_password_checkbox.grid(row=5, column=0, padx=50, pady=10, sticky="w")

# Change Password button
change_button = ctk.CTkButton(left_frame, text="Change Password", width=300, height=40, fg_color="#1B5671", text_color="white",
                              font=("Arial", 16, "bold"), command=lambda: change_password())
change_button.grid(row=6, column=0, padx=50, pady=(30, 20), sticky="w")

# Right side banner
car_image = resize_image((600, 1200), 'images/loginBanner.jpg')
car_label = ctk.CTkLabel(password_change_window, text="", image=car_image)
car_label.place(x=500, y=0)

# Password change function
def change_password():
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Validate inputs
    if not new_password or not confirm_password:
        messagebox.showerror("Error", "All fields are required")
        return

    if new_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    # Basic password validation
    if len(new_password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Update the user's password and status in the users table
        cursor.execute("UPDATE users SET password = %s, status = 'active' WHERE email = %s AND password = %s",
                       (new_password, email, current_password))
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Failed to update password. Please try again.")
            return

        conn.commit()

        # Get the user's role to redirect to the appropriate dashboard
        cursor.execute("SELECT role_id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found")
            return

        role_id = user[0]
        role_map = {1: 'admin', 2: 'staff', 3: 'customer'}
        role_name = role_map.get(role_id, 'customer')

        messagebox.showinfo("Success", "Password changed successfully. You will be redirected to your dashboard.")
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), f"{role_name}_dashboard.py"), email])
        password_change_window.destroy()

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to change password: {e}")
    finally:
        cursor.close()
        conn.close()

password_change_window.mainloop()