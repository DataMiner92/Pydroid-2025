import tkinter as tk
from tkinter import messagebox
import requests

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
API_KEY = '0f1dc808ffed15e683d121fdb79f636a'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    params = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        
        city = weather_data['name']
        country = weather_data['sys']['country']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        weather_description = weather_data['weather'][0]['description']
        
        return (f"City: {city}, {country}\n"
                f"Temperature: {temp}°C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s\n"
                f"Weather: {weather_description.capitalize()}")
    except requests.RequestException as e:
        return f"Error: {e}"

def show_weather():
    city_name = city_entry.get()
    if city_name:
        weather_info = get_weather(city_name)
        weather_label.config(text=weather_info)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")

# Create main window
root = tk.Tk()
root.title("Weather App")

# City input
city_label = tk.Label(root, text="Enter city name:")
city_label.pack(pady=10)
city_entry = tk.Entry(root, width=50)
city_entry.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Get Weather", command=show_weather)
search_button.pack(pady=10)

# Weather info display
weather_label = tk.Label(root, text="", justify='left', font=("Helvetica", 12))
weather_label.pack(pady=20)

# Run the application
root.mainloop()