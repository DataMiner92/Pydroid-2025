import tkinter as tk
from tkinter import messagebox

def calculate():
    x = int(entry1.get())
    y = int(entry2.get())
    choice = choice_var.get()

    if choice == 1:
        result = x * y
    elif choice == 2:
        result = x + y
    elif choice == 3:
        if y != 0:
            result = x / y
        else:
            messagebox.showerror("Error", "Cannot divide by zero!")
            return
    elif choice == 4:
        result = y * y
    elif choice == 5:
        result = x ** y
    else:
            
            return

    result_label.config(text=f"Result: {result}")

def on_exit():
    root.destroy()

root = tk.Tk()
root.title("Simple Calculator")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

choice_var = tk.IntVar()
choice_var.set(1)

tk.Label(frame, text="Select operation:").grid(row=0, column=0, sticky="w")
tk.Radiobutton(frame, text="Multiply", variable=choice_var, value=1).grid(row=1, column=0, sticky="w")
tk.Radiobutton(frame, text="Add", variable=choice_var, value=2).grid(row=2, column=0, sticky="w")
tk.Radiobutton(frame, text="Divide", variable=choice_var, value=3).grid(row=3, column=0, sticky="w")
tk.Radiobutton(frame, text="Square", variable=choice_var, value=4).grid(row=4, column=0, sticky="w")

tk.Radiobutton(frame, text="Power", variable=choice_var, value=5).grid(row=5, column=0, sticky="w")

tk.Label(frame, text="Enter first number:").grid(row=6, column=0, sticky="w")
entry1 = tk.Entry(frame)
entry1.grid(row=6, column=1)

tk.Label(frame, text="Enter second number:").grid(row=7, column=0, sticky="w")
entry2 = tk.Entry(frame)
entry2.grid(row=7, column=1)

calculate_button = tk.Button(frame, text="Calculate", command=calculate)
calculate_button.grid(row=8, column=0, columnspan=2, pady=20)

result_label = tk.Label(frame, text="Result:")
result_label.grid(row=10, column=0, columnspan=2)

exit_button = tk.Button(frame, text="Exit", command=on_exit)
exit_button.grid(row=11, column=0, columnspan=2, pady=20)

root.mainloop()
