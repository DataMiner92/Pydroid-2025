import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser


window = tk.Tk()
window.geometry("700x750")
window.title("One-Stop Shop")
window.configure(bg="orange")

def main_menu():
    try:
        info = simpledialog.askstring("Main Menu", "1. Log In\nSelect: ")
        if info == "1":
            user = simpledialog.askstring("Login", "1. Guest\n2. Resident\nSelect: ")
            if user == "1":
                guest_login()
            elif user == "2":
                access_prompt()
            else:
                messagebox.showerror("Error", "Invalid Selection!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def guest_login():
    try:
        password = "12345"
        log = simpledialog.askstring("Login Guest", "Enter Password: ", show='*')
        if log == password:
            messagebox.showinfo("Guest Login", "Log in was Successful!")
        else:
            messagebox.showerror("Guest Login", "Incorrect Password!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def access_prompt():
    try:
        prompt = simpledialog.askstring("Services", "1. Create Own Account\n2. Register")
        if prompt == "1":
            simpledialog.askstring("Create password", "Create Password: ")
            response = messagebox.askquestion("Password", "Do you want to save password?")
        elif prompt == "2":
                messagebox.showinfo("Services", "1. Forgot Password. \n 2. Reset")
                simpledialog.askstring("Services", "1. Enter Email address: ")
                response = messagebox.showinfo("Services", "Reset was Successful")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def exit_menu():
    window.destroy()


show_button = tk.Button(window, text="Access", bg="orange", command=main_menu)
show_button.grid(row=0, column=4, padx=25, pady=5)


window.mainloop()