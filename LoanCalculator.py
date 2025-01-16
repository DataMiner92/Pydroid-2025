import tkinter  as tk
from tkinter.font import Font
from datetime import datetime 
import requests
from datetime import time

 
window = tk.Tk()
window.title("💰My Loan App🏆")

def calculate_loan():
         amount = float(amount_entry.get())
         time = int(time_entry.get())
         interest = 0.08
         loan = amount * interest * time + amount
         result_label.config(text="Your Payback Loan Amount is KES: {:.2f}".format(loan))
         
         date = datetime.now().strftime("%Y-%m-%d %I:%M %p")
         date_label.config(text="Time is: {}".format(date))
         
custom_font = Font(family="Times New Roman", size=12, weight="bold")

custom = Font(family="Arial", size=9, weight="bold")

custom_emoji = Font(family="Segoe UI Emoji", size=9, weight="bold")

main_label = tk.Label(window, text="Umoja Loan App©2024", font=custom_font)
main_label.grid(row=0, column=0, columnspan=2, padx=10,  pady=5)

amount_label = tk.Label(window, text="Enter Amount (Kes): ", font=custom)
amount_label.grid(row=1, column=0, padx=0, pady=5)

amount_entry = tk. Entry(window)
amount_entry.grid(row=1, column=1, padx=10, pady=5)


time_label = tk.Label(window, text="Repay Time (Years): ", font=custom)
time_label.grid(row=2, column=0, padx=10, pady=10)

time_entry = tk. Entry(window)
time_entry.grid(row=2, column=1, padx=0, pady=5)

calculate_button = tk.Button(window, text ="Calculate Loan", command=calculate_loan, font=custom)
calculate_button.grid(row=3, columnspan=4, padx=5, pady=5)

result_label = tk.Label(window, text="")
result_label.grid(row=5, column=0, columnspan=4, padx=10,  pady=5)

def on_exit():
    window.destroy()
    
exit_button = tk.Button(window, text="Exit", command=on_exit)
exit_button.grid(row=23, columnspan=4, padx=5, pady=5)

contact_label = tk.Label(window, text="Contact Us: Umojaloan@zoho.com", font=custom)
contact_label.grid(row=45, column=0, columnspan=4, padx=10,  pady=5)


date_label = tk.Label(window, text="")
date_label.grid(row=35, column=0, columnspan=4, padx=10,  pady=5)

window.mainloop()
         