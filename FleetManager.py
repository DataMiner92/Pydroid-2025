import tkinter as tk
from itertools import cycle
import tkinter 



class FleetManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Super Metro Management")

        # Define routes and buses
        self.routes = ['Ngong', 'Kitengela', 'Rongai', 'Kikuyu', 'Makongeni', 'Juja']
        self.buses = ['101A', '102B', '103C', '104D', '105E', '106F', '107G', '108H']

        # Create a cycle iterator for routes to loop through them
        self.route_iterator = cycle(self.routes)

        # Create a dictionary to store the schedule for each bus
        self.schedule = {bus: [] for bus in self.buses}

        # Simulate 8 trips per day for each bus
        self.simulate_trips()

        # Create GUI elements
        self.label = tk.Label(master, text="Enter Bus Registration Number:", bg="Orange")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.button = tk.Button(master, text="Show Routes", command=self.show_routes, bg="orange")
        self.button.pack()

    def simulate_trips(self):
        for _ in range(8):
            for bus in self.buses:
                route = next(self.route_iterator)
                self.schedule[bus].append(route)

    def show_routes(self):
        registration_number = self.entry.get().strip()
        if registration_number in self.schedule:
            assigned_routes = self.schedule[registration_number]
            result = f"Routes assigned to {registration_number}: \n{','.join(assigned_routes)}"
        else:
            result = "Invalid registration number.\n Please enter a valid registration number."

        result_label = tk.Label(self.master, text=result, wraplength=300)
       
        result_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="gray")
    app = FleetManagementApp(root)
    root.mainloop()
    