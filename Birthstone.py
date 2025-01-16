import tkinter as tk
from tkinter.font import Font

month_list = {
    "January": {"B_stone": "Garnet", "Flower": "Carnation"},
    "February": {"B_stone": "Amethyst", "Flower": "Violet"}
}

def search_birthstone():
    month_name = entry.get()
    if month_name in month_list:
        month_info = month_list[month_name]
        result_label.config(text=f"B_stone: {month_info['B_stone']},\nFlower: {month_info['Flower']}")
    else:
        result_label.config(text="Sorry, Month not found! Capitalize first letter.")

def exit_button():
    root.destroy()

root = tk.Tk()
root.title("Birthstone and Flower")
root.configure(bg="Yellow")

custom_font = Font(family="Arial", size=12, weight="bold")

label = tk.Label(root, text="Enter month:", font=custom_font, bg="cyan")
label.pack()
entry = tk.Entry(root)
entry.pack(pady=20)

search_button = tk.Button(root, text="Search", command=search_birthstone)
search_button.pack(pady=20)

result_label = tk.Label(root, text="")
result_label.pack(pady=20)

button_exit = tk.Button(root, text="Exit", command=exit_button)
button_exit.pack(pady=20)

root.mainloop()