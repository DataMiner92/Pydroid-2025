import tkinter as tk

def animate_text():
    global x_pos
    canvas.delete("text") 
    canvas.create_text(x_pos, 50, text="It's Too Early to Quit \n Take Charge", fill="green", font=('Calligraphy', 24), tag="text")
    x_pos += 5  
    if x_pos > window.winfo_width():
        x_pos = 0  
    window.after(50, animate_text) 

window = tk.Tk()
window.title("Scrollin")
window.configure(bg="orange")

x_pos = 0
canvas = tk.Canvas(window, width=500, height=300)
canvas.pack()

animate_text()

window.mainloop()