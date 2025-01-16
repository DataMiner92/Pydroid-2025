import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from datetime import datetime
import secrets
import string
import random

def generate_random_code(length=10):
    characters = string.ascii_uppercase
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code  

def mpesa_service():
    select = messagebox.askquestion("M-Pesa Services", "1. Send Money\n2. Withdraw Money\nSelect choice:")
    if select == 'yes':
        choice = simpledialog.askstring("M-Pesa Services", "Enter your choice (1 or 2):")
        if choice == "1":
            user = simpledialog.askstring("M-Pesa Services", "Enter amount to send:")
            phone = random.randint(700000000, 1111111111)
            confirm_transaction(user, phone)
        elif choice == "2":
            user = simpledialog.askstring("M-Pesa Services", "Enter amount to withdraw:")
            confirm_withdrawal(user)
        else:
            messagebox.showerror("Error", "Invalid input. Select 1 or 2.")

def confirm_transaction(amount, phone):
    code = generate_random_code()
    balance = random.randint(999, 99999)
    time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    messagebox.showinfo("Confirmation", f"{code} Confirmed. \n KES {amount} sent to {phone}. \n New MPESA balance is KES {balance} \n on {time}.")

def confirm_withdrawal(amount):
    code = generate_random_code()
    balance = random.randint(999, 999999)
    time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    messagebox.showinfo("Confirmation", f"{code} Confirmed. \n You've withdrawn KES {amount}. \n Your new balance is KES {balance} \n at {time}")


def confirm_airtime(amount, phone):
    code = generate_random_code()
    balance = random.randint(9, 999)
    time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    messagebox.showinfo("Confirmation", f"Confirmed. \n KES {amount} sent to {phone}. \n New Airtime balance is KES {balance} \n on {time}.")
    
def bank_confirm(user):
       balance = random.randint(9, 999999)
       time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
       messagebox.showinfo("Confirmation", f"Confirmed. \n KES {user}  withdrawn to {phone}. \n New Account balance is KES {balance} \n on {time}.")

def other_services():
     pick = messagebox.askquestion("M-Pesa Services", "1. Airtime \n2. Banking\nSelect choice:")
     if pick == 'yes':
        choice = simpledialog.askstring("M-Pesa Services", "Enter your choice (1 or 2):")
        if choice == "1":
            user = simpledialog.askstring("M-Pesa Services", "Enter amount of airtime to send:")
            phone = random.randint(700000000, 1111111111)
            confirm_airtime(user, phone)
        if choice == "2":
            user =  messagebox.askquestion("M-Pesa Services", "1. Equity\n2. Family Bank\n3. CBA\n4. KCB\n5. Select choice:")
            if pick == 'yes':
                choice = simpledialog.askstring("M-Pesa Services", "Enter your choice (1 or 2):")
                if choice == "2":
                    user = simpledialog.askstring("M-Pesa Services", "Enter amount to withdraw:")
                bank_confirm(user)

 
root = tk.Tk()
root.title("M-Pesa Services")

     
def exit_button():
     root.destroy()

button = tk.Button(root, text="M-Pesa", command=mpesa_service)
button.pack(pady=10)

button = tk.Button(root, text="Other Services", command=other_services)
button.pack(pady=20)

button_exit = tk.Button(root, text ="Exit", command=exit_button)
button.pack(pady=30)

root.mainloop()
