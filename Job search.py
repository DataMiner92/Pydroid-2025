import tkinter as tk
from tkinter import messagebox
import requests

# Function to search for jobs
def search_jobs():
    query = entry.get()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a job title.")
        return

    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": "b86e5cf1",
        "app_key": "57a31116deb5b1c675ea9d9beb41b10c",
        "results_per_page": 4,
        "what": query,
        "where": "Africa"
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        jobs = response.json().get('results', [])
        display_jobs(jobs)
    else:
        messagebox.showerror("API Error", "Failed to fetch jobs. Please try again.")

# Function to display job results
def display_jobs(jobs):
    result_text.delete(1.0, tk.END)
    if not jobs:
        result_text.insert(tk.END, "No jobs found.")
    else:
        for job in jobs:
            result_text.insert(tk.END, f"Title: {job['title']}\nCompany: {job['company']['display_name']}\nLocation: {job['location']['display_name']}\nLink: {job['redirect_url']}\n\n")

# Create the main window
root = tk.Tk()
root.title("Job Search")
root.geometry("700x2800")
root.configure(bg="gray")

# Create and place widgets
label = tk.Label(root, text="Enter Job Title:", bg="orange")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search Jobs", command=search_jobs, bg="orange")
search_button.pack(pady=5)

result_text = tk.Text(root, height=20, width=100, bg="cyan")
result_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()