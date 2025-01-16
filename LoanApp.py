import tkinter as tk
from tkinter.font import Font
from datetime import datetime

window = tk.Tk()
window.geometry("700x550")
window.title("💰 My Loan App 🏆")
window.configure(bg="dark gray")  # Set a neutral background color for better readability

def calculate_loan():
    try:
        amount = float(amount_entry.get())
        time = int(time_entry.get())
        
        if amount <= 0 or time <= 0:
            raise ValueError("Amount and time must be positive numbers.")
        
        interest = 0.08
        loan = amount * interest * time + amount
        result_label.config(text="Your Payback Loan Amount is KES: {:.2f}".format(loan))
    except ValueError as e:
        result_label.config(text=str(e))
    
    # Update date and time
    date = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    date_label.config(text="Time is: {}".format(date))

custom_font = Font(family="Comic Sans MS", size=10, weight="bold")
custom = Font(family="Comic Sans MS", size=10, weight="bold")

main_label = tk.Label(window, text="Umoja Loan App ©2024", font=custom_font, bg="gold")
main_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

amount_label = tk.Label(window, text="Enter Amount (Kes): ", font=custom)
amount_label.grid(row=1, column=0, padx=0, pady=5)

amount_entry = tk.Entry(window)
amount_entry.grid(row=1, column=1, padx=10, pady=10)

time_label = tk.Label(window, text="Repay Time (Years): ", font=custom)
time_label.grid(row=2, column=0, padx=10, pady=10)

time_entry = tk.Entry(window)
time_entry.grid(row=2, column=1, padx=0, pady=5)

calculate_button = tk.Button(window, text="Calculate Loan", command=calculate_loan, font=custom, bg="cyan")
calculate_button.grid(row=3, columnspan=4, padx=5, pady=5)

result_label = tk.Label(window, text="", font=custom, bg="#F0F0F0") 
result_label.grid(row=5, column=0, columnspan=4, padx=10, pady=5)

def on_exit():
    window.destroy()
    
exit_button = tk.Button(window, text="Exit", command=on_exit, font=custom, bg="orange")
exit_button.grid(row=30, columnspan=4, padx=5, pady=5)

contact_label = tk.Label(window, text="Contact Us: Umojaloan@zoho.com", font=custom, bg="dark gray")
contact_label.grid(row=45, column=0, columnspan=4, padx=10, pady=5)

date_label = tk.Label(window, text="", bg="#F0F0F0")  # Set a neutral background color for the date label
date_label.grid(row=35, column=0, columnspan=4, padx=10, pady=5)

window.mainloop()