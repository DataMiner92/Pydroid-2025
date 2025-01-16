import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog
import webbrowser

window = tk.Tk()

window.geometry("700x750")
window.title("One-Stop Shop")
window.configure(bg="orange")

def main_menu():
    info = simpledialog.askstring("Main Menu", "1. Log In\n Select: ")
    if info == "1":
        user = simpledialog.askstring("Login", "1. Geust\n2. Resident\n Select: ")
        if user == "1":
            password = "12345"
            log = simpledialog.askstring("Login Guest", "Enter Password: ")
            if log == password:
                show = messagebox.showinfo("Guest Login", "Log in was Successful!")
                if log != password:
                         messagebox.showerror("Guest Login", "Incorrect Password!")
                        
                         
def   access_prompt():
    prompt = messagebox.showinfo("Services", "1. Create Own Account.\n 2. Register.")                                                      
                                                          
                                              
def exit_menu():
 window.destroy()

def open_url(url):
 webbrowser.open_new(url)

def on_enter(event, button):
    button['bg'] ='cyan'
    
def on_leave(event, button):
    button['bg'] ='gray'
    

    
    
show_button = tk.Button(window, text="Access", bg="orange", command=main_menu)
show_button.grid(row=0, column=0, padx=5, pady=5)


show_button = tk.Button(window, text="User", bg="orange", command=access_prompt)
show_button.grid(row=0, column=1, padx=5, pady=5)

show_button = tk.Button(window, text="Google", bg="orange", command=lambda: open_url("https://www.google.com"))
show_button.grid(row=0, column=2, padx=5, pady=5)

show_button = tk.Button(window, text="CBK", bg="orange",  command=lambda: open_url("https://whatsapp.com/channel/0029Va5HrcD4dTnNnTguwc24"))
show_button.grid(row=2, column=0, padx=10, pady=5)

show_button = tk.Button(window, text="Chat GPT", bg="orange", command=lambda: open_url("https://chatgpt.com"))
show_button.grid(row=2, column=1, padx=10, pady=5)

show_button = tk.Button(window, text="Jumia", bg="orange", command=lambda: open_url("https://jumia.co.ke"))
show_button.grid(row=2, column=2, padx=10, pady=5)


show_button = tk.Button(window, text="Jiji", bg="orange", command=lambda: open_url("https://www.jiji.co.ke"))
show_button.grid(row=3, column=0, padx=5, pady=10)


show_button = tk.Button(window, text="Mdundo", bg="orange", command=lambda: open_url("https://www.mdundo.com/ke"))
show_button.grid(row=3, column=1, padx=5, pady=10)


show_button = tk.Button(window, text="Bing", bg="orange", command=lambda: open_url("https://www.bing.com"))
show_button.grid(row=3, column=2, padx=5, pady=10)



show_button = tk.Button(window, text="News", bg="orange", command=lambda: open_url("https://www.msn.com"))
show_button.grid(row=0, column=3, padx=5, pady=10)

exit_button = tk.Button(window, text="Exit", bg="red", command=exit_menu)
exit_button.grid(row=5, column=1, padx=5, pady=5 )


window.mainloop()