import tkinter as tk
from tkinter import messagebox

def evaluate_score():
    score_str = entry.get()
    
    try:
        score = int(score_str)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid integer score.")
    else:
        if 90 <= score <= 100:
            messagebox.showinfo("Result", "You need to read:\n 1. About the Struggle \n 2. The 2 Lies, \n 3. 3 Things about Life.")
            messagebox.askquestion("Proceed", "Do you want to continue?")
        elif 75 <= score < 90:
            messagebox.showinfo("Result", "1. Home Stretch\n 2. Enemy of the People \n 3. Betrayal in the City.")
        elif 55 <= score < 75:
            messagebox.showinfo("Result", "1. Business & Power \n 2. Money Matters")
        elif 40 <= score < 55:
            messagebox.showinfo("Result", "1. Asset Liquidity \n 2. Communication Skills")
        elif 1<= score <39:
            messagebox.showinfo("Result", "1. The Last Street \n 2. Wisdom of the Crowd.")
        else:
            choice = messagebox.askquestion("Proceed", "Do you want to proceed?")
            if choice == "yes":
                return score
                


def exit_window():
    window.destroy()
    
    
window = tk.Tk()
window.title("Gamers")
window.configure(bg="orange")
window.geometry("700x550")


label = tk.Label(window, text="Enter score:", bg="orange")
label.pack(pady=10)


entry = tk.Entry(window)
entry.pack(pady=10)

submit_button = tk.Button(window, text="Submit", command=evaluate_score, bg="gray")
submit_button.pack(pady=20)


exit_button = tk.Button(window, text="Exit", command=exit_window, bg="green")
exit_button.pack()



window.mainloop()