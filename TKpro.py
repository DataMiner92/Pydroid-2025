import tkinter as tk

def display_websites():
    websites = [
        "https://www.google.com",
        "https://www.domain.com",
        "https://www.bing.com",
        "https://www.openchat.com",
        "https://www.plotterai.com",
        
    ]
    websites_window = tk.Toplevel(root)
    websites_window.title("Web Links")
    website_listbox = tk.Listbox(websites_window)
    for website in websites:
        website_listbox.insert(tk.END, website)
    website_listbox.pack()

def display_services_menu():
    services = [
        "Marketing",
        "Branding",
        "Web Development",
        "Graphic Design",
        "Artificial Intelligence ",
        "Local Host",
        "Cyber Security ",
        "Web Domain",
        "UX Design",
        "Data Science",
       
    ]
    services_window = tk.Toplevel(root)
    services_window.title("Services")
    services_listbox = tk.Listbox(services_window)
    for service in services:
        services_listbox.insert(tk.END, service)
    services_listbox.pack()


root = tk.Tk()
root.title("Optimus Link")


website_button = tk.Button(root, text="Links", command=display_websites)
website_button.pack(pady=20)

services_button = tk.Button(root, text="Products", command=display_services_menu)
services_button.pack(pady=20)

exit_button =tk.Button(root, text = "Exit", command=root.destroy)
exit_button.pack(pady=20)

root.mainloop()

