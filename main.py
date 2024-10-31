import tkinter as tk
from tkinter import messagebox

def login():
    username = entry.get()
    # Here you would typically add your logic to connect to the database
    # and fetch user data
    messagebox.showinfo("Login", f"Welcome, {username}!")

# Create the main application window
root = tk.Tk()
root.title("Login Application")

# Create and place widgets
label = tk.Label(root, text="Enter your screen name:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)

# Start the application
root.mainloop()
