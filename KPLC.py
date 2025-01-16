import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
window = tk.Tk()
window.title("Prepaid Meter")
root.geometry()

def display_menu():
    
    payload = int(payload_entry.get())
    meter = int(meter_entry.get())

def services_menu():
    token = messagebox.showinfo("Load Token")
    ask = messagebox.askquestion("What can do for you?")
    confirm = message box.askokcancel("Ok/Cancel", "Press OK to Continue, No to Stop")
    
    
 
     
button_menu=tk.Button(root, text = "Menu", command=display_menu)
button_menu.pack(pady=20)


button_service=tk.Button(root, text = "Services", command=services_menu)
button_service.pack(pady=20)


exit_button =tk.Button(root, text = "Exit", command=root.destroy)
exit_button.pack(pady=20)

window.mainloop()

root.mainloop()


