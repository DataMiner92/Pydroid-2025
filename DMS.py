import tkinter 
from tkinter import ttk
from tkinter import messagebox

window = tkinter.Tk()
window.title("DMS Form")

frame = tkinter.Frame(window)
frame.pack()

client_info_frame = tkinter.LabelFrame(frame, text="Client Profile")
client_info_frame.grid(row=0, column=0, padx=5, pady=5)

first_name_label = tkinter.Label(client_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)


last_name_label = tkinter.Label(client_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(client_info_frame)

last_name_entry = tkinter.Entry(client_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)


occupation_label = tkinter.Label(client_info_frame, text="Occupation")
occupation_combobox = ttk.Combobox(client_info_frame, values=["Engineer", "Teacher", "Doctor", "Carpenter", "Social Worker"])
occupation_label.grid(row=3, column=0)
occupation_combobox.grid(row=3, column=1)

for widget in client_info_frame.winfo_children():
    widget.grid_configure(padx=1, pady=1)


def save_info():
    first_name = first_name_entry()
    last_name = last_name_entry()
    occupation_info = occupation_combox_values
    


window.mainloop()
