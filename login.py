#login.py
import sys
import os
import tkinter as tk
import customtkinter as ctk
from utils import resize_image, authenticate_user
from constants import COLORS
import subprocess
from tkinter import messagebox

# Configure CustomTkinter Theme
ctk.set_appearance_mode("light")

# Initialize the main window
login_window = ctk.CTk()
login_window.title("Login - QuickDrive Rentals")
login_window.geometry("800x600")
login_window.resizable(False, False)
login_window.configure(fg_color=COLORS['color_1'])

# Login form
left_frame = ctk.CTkFrame(login_window, fg_color=COLORS['color_2'], width=400, height=400)
left_frame.pack_propagate(False)
left_frame.place(x=50, y=100)

# Logo at the top-left
logo_image = resize_image((100, 50), 'images/loginLogo.jpg')
logo_label = ctk.CTkLabel(login_window, text="", image=logo_image)
logo_label.place(x=20, y=20)

#Logo Title
logotitle_label = ctk.CTkLabel(login_window, text="QuickDrive Rentals", font=("Aclonica", 16, "bold"), text_color="white")
logotitle_label.place(x=90, y=20)

# Login form title
login_title = ctk.CTkLabel(left_frame, text="Login", font=("Abril Fatface", 18, "bold"), text_color="black")
login_title.place(x=170, y=50)

# Email input
username_label = ctk.CTkLabel(left_frame, text="Email", font=("Abril Fatface", 14, "bold"), text_color="black")
username_label.place(x=50, y=100)
username_entry = ctk.CTkEntry(left_frame, width=300, height=35, border_color="black", border_width=1, placeholder_text="abc@gmail.com")
username_entry.place(x=50, y=130)

# Password input
password_label = ctk.CTkLabel(left_frame, text="Password", font=("Abril Fatface", 14, "bold"), text_color="black")
password_label.place(x=50, y=200)
password_entry = ctk.CTkEntry(left_frame, show="*", width=300, height=35, border_color="black", border_width=1, placeholder_text="password")
password_entry.place(x=50, y=230)

# Remember me and Show Password checkboxes
show_password_var = ctk.StringVar()
remember_me = ctk.CTkCheckBox(left_frame, text="Remember me", text_color="black")
remember_me.place(x=50, y=275)
show_password_checkbox = ctk.CTkCheckBox(left_frame, text="Show Password", variable=show_password_var, onvalue="on", offvalue="off", command=lambda: password_entry.configure(show="" if show_password_var.get() == "on" else "*"), text_color="black")
show_password_checkbox.place(x=220, y=275)

# Login button
login_button = ctk.CTkButton(left_frame, text="Login", width=300, height=40, fg_color="#1B5671", text_color="white", font=("Arial", 16, "bold"), command=lambda: on_login_click())
login_button.place(x=50, y=320)

# Signup link
signup_label = ctk.CTkLabel(left_frame, text="Don't have an account?", font=("Arial", 12), text_color="black")
signup_label.place(x=100, y=360)
signup_link = ctk.CTkLabel(left_frame, text="Signup", font=("Arial", 12, "bold"), text_color="black", cursor="hand2")
signup_link.place(x=227, y=360)
signup_link.bind("<Button-1>", lambda event: subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "signup.py")]) and login_window.destroy())

# Right side - Car image banner
car_image = resize_image((600, 1200), 'images/loginBanner.jpg')
car_label = ctk.CTkLabel(login_window, text="", image=car_image)
car_label.place(x=500, y=0)

# Login function
def on_login_click():
    email = username_entry.get()
    password = password_entry.get()
    if not email or not password:
        messagebox.showerror("Error", "You must enter values for email and password")
        return
    user = authenticate_user(email, password)
    if user[0]:
        if user[1] == "Password Change Required":
            messagebox.showinfo("Information", "Password Change Required")
            subprocess.Popen([sys.executable, os.path.join(os.getcwd(), 'password_change.py'), email, password])
            login_window.destroy()
        else:
            role = user[0][5]
            role_map = {1: 'admin', 2: 'staff', 3: 'customer'}
            role_name = role_map.get(role, 'customer')
            subprocess.Popen([sys.executable, os.path.join(os.getcwd(), f"{role_name}_dashboard.py"), email])
            login_window.destroy()
    else:
        messagebox.showerror("Error", user[1])

login_window.mainloop()
