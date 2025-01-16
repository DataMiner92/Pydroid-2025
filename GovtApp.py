import tkinter as tk
import webbrowser

def open_url(url):
    webbrowser.open_new(url)

# Function to change the button color on hover
def on_enter(event, button):
    button['bg'] = 'lightblue'

# Function to revert the button color when the mouse leaves
def on_leave(event, button):
    button['bg'] = 'cyan'

# Create the main window
window = tk.Tk()
window.title("URL Opener")
window.configure(bg="#F0F0F0")

# Define a custom font for the buttons
custom_font = ("Comic Sans MS", 12, "bold")

# Create a label
main_label = tk.Label(window, text="Click a button to open a URL", font=custom_font, bg="gold")
main_label.pack(pady=10)

# Create buttons to open different URLs and bind the hover events
buttons = [
    {"text": "Open Google", "url": "https://www.google.com"},
    {"text": "Open GitHub", "url": "https://www.github.com"},
    {"text": "Open Stack Overflow", "url": "https://stackoverflow.com"}
]

for button_info in buttons:
    button = tk.Button(window, text=button_info["text"], font=custom_font, bg="cyan", command=lambda url=button_info["url"]: open_url(url))
    button.pack(pady=5)
    button.bind("<Enter>", lambda event, btn=button: on_enter(event, btn))
    button.bind("<Leave>", lambda event, btn=button: on_leave(event, btn))

# Start the Tkinter event loop
window.mainloop()