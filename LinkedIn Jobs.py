import tkinter as tk
from tkinter import messagebox
import requests

# Function to search for jobs
def search_jobs():
    query = entry.get()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a job title.")
        return

    url = "https://www.linkedin.com/jobs/search"
    querystring = {"keywords": query, "location": "Africa", "start": "0", "count": "10"}

    headers = {
        "X-RapidAPI-Key": "d82aa46a17msh1e96a6afbea9fcep11fab4jsn2cf1ee6e184e",
        "X-RapidAPI-Host": "linkedin-jobs-api.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        jobs = response.json().get('data', [])
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
            result_text.insert(tk.END, f"Title: {job['title']}\nCompany: {job['company']}\nLocation: {job['location']}\nLink: {job['jobLink']}\n\n")

# Create the main window
root = tk.Tk()
root.title("LinkedIn Job Search")
root.geometry("700x700")

# Create and place widgets
label = tk.Label(root, text="Enter Job Title:")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search Jobs", command=search_jobs)
search_button.pack(pady=5)

result_text = tk.Text(root, height=20, width=100)
result_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()