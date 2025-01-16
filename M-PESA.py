import tkinter as tk

root = tk.Tk()
root.title("Simulator")
root.geometry()

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label = tk.Label(root, text="~~Welcome to M-Pesa Services Menu~~")
label.pack(pady=20)

def display_mpesa_subservices():
    mpesa_subservices = [
        "1. Send Money",
        "2. Withdraw Cash",
        "3. Lipa Na M-PESA"
    ]
    subservices_window = tk.Toplevel(root)
    subservices_window.title("M-PESA Subservices")
    subservices_window.geometry(f"300x200+{root.winfo_screenwidth() // 2 - 150}+{root.winfo_screenheight() // 2 - 100}")
    subservices_listbox = tk.Listbox(subservices_window)
    for subservice in mpesa_subservices:
        subservices_listbox.insert(tk.END, subservice)
    subservices_listbox.pack()


def display_kcb_mpesa_subservices():
    kcb_mpesa_subservices = [
        "1. Deposit",
        "2. Withdraw",
        "3. Check Balance"
    ]
    subservices_window = tk.Toplevel(root)
    subservices_window.title("KCB M-PESA Subservices")
    subservices_window.geometry(f"300x200+{root.winfo_screenwidth() // 2 - 150}+{root.winfo_screenheight() // 2 - 100}")
    subservices_listbox = tk.Listbox(subservices_window)
    for subservice in kcb_mpesa_subservices:
        subservices_listbox.insert(tk.END, subservice)
    subservices_listbox.pack()


def display_services_menu():
    services = [
        ("M-PESA", display_mpesa_subservices),
        ("KCB MPESA", display_kcb_mpesa_subservices)
    ]
    services_window = tk.Toplevel(root)
    services_window.title("Services")
    for service, command in services:
        button = tk.Button(services_window, text=service, command=command)
        button.pack()


click_button = tk.Button(root, text="Click Here", command=display_services_menu)
click_button.pack(pady=20)

exit_button = tk.Button(root, text="Exit!", command=root.destroy)
exit_button.pack(pady=20)

root.mainloop()
