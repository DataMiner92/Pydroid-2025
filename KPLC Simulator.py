import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import secrets
import string
import random

def generate_random_code(length=10):
    characters = string.ascii_uppercase
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code  

def is_valid_voucher(voucher):
    return len(voucher) == 20 and voucher.isdigit()

def is_valid_meter(meter):
    return len(meter) == 10 and meter.isdigit()
def is_valid_share_id(share_id):
    return len(share_id) == 10 and share_id.isdigit()

def kplc_service():
    select = messagebox.askquestion("KPLC Self Service", "1. Load Token\n2. Share Token\nSelect choice:")
    if select == 'yes':
        choice = simpledialog.askstring("KPLC Self Service", "Enter your choice (1 or 2):")
        if choice == "1":
            voucher = simpledialog.askstring("KPLC Self Service", "Enter Token Voucher:")
            if is_valid_voucher(voucher):
                meter_no =  simpledialog.askstring("KPLC Self Service", "Enter Valid Meter No:")
                units = random.randint(1, 1000)
                confirm_transaction(voucher, meter_no, units)
            else:
                messagebox.showerror("Error", "Invalid voucher number.")
        elif choice == "2":
            units = simpledialog.askstring("KPLC Self Service", "Enter amount of units to share:")
            share_id = simpledialog.askstring("KPLC Self Service", "Enter Valid Meter No of Reciever:")
            confirm_share(units)
        else:
            messagebox.showerror("Error", "Invalid input. Select 1 or 2.")

def confirm_transaction(voucher, meter_no, units):
    code = generate_random_code()
    time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    message = f"{code} Confirmed. \n {units} units loaded to MtrNo {meter_no} \n on {time}"
    messagebox.showinfo("Confirmation", message)

def confirm_share(units):
    code = generate_random_code()
    balance = random.randint(9,999)
    time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    share_id = simpledialog.askstring("KPLC Self Service", "Enter Valid Meter No of Reciever:")
    message = f"{code} Confirmed. \n You've shared {units} units with \n mtrNo {share_id}. \n Your balance is {balance} units at \n {time}."
    messagebox.showinfo("Confirmation", message)


root = tk.Tk()
root.title("KPLC Self Service")

button = tk.Button(root, text="KPLC Access", command=kplc_service)
button.pack(pady=20)

button_exit = tk.Button(root, text="Exit", command=root.destroy)
button_exit.pack(pady=20)

root.mainloop()



