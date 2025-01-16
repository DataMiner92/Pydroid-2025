import tkinter as tk

def calculate_bmi():
    weight = float(weight_entry.get())
    height = float(height_entry.get())
    bmi = weight / (height ** 2)
    result_label.config(text="Your BMI is: {: .2f}". format(bmi))
    
def exit ():
    window.destroy()
    
window = tk.Tk()
window.title("BMI Calculator")
window.configure(bg="magenta")


weight_label = tk.Label(window, text="Weight (kg): ")
weight_label.grid(row=0, column=0, padx=10, pady=5)
weight_entry = tk.Entry(window)
weight_entry.grid(row=0, column=1, padx=10, pady=5)


height_label = tk.Label(window, text="Height (m): ")
height_label.grid(row=1, column=0, padx=10, pady=5)
height_entry = tk.Entry(window)
height_entry.grid(row=1, column=1, padx=10, pady=5)

calculate_button = tk.Button(window, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)


exit_button = tk.Button(window, text="Exit", command=exit)
exit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)


result_label = tk.Label(window, text="")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)




window.mainloop()