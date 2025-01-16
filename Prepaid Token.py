import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
window = tk.Tk()
window.title("Prepaid Meter")
root.geometry()

def display_menu():
    print("Loading..")
    token = messagebox.showinfo("Load Token")
    
 
     
button_menu=tk.Button(root, text = "Menu", command=display_menu)
button_menu.pack(pady=20)

exit_button =tk.Button(root, text = "Exit", command=root.destroy)
exit_button.pack(pady=20)

window.mainloop()

root.mainloop()


