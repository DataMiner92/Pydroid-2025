import random
import time

# Function to read temperature and humidity from sensors
def read_sensor_data():
    # Simulating sensor data
    temperature = round(random.uniform(20.0, 30.0), 2)
    humidity = round(random.uniform(40.0, 70.0), 2)
    return temperature, humidity

# Function to get feeding schedule
def get_feeding_schedule():
    feeding_schedule = {
        "Morning": "8:00 AM",
        "Afternoon": "2:00 PM",
        "Evening": "6:00 PM"
    }
    return feeding_schedule

# Main loop to continuously monitor and display data
while True:
    temperature, humidity = read_sensor_data()
    feeding_schedule = get_feeding_schedule()

    # Displaying data on the IoT interface
    print("Greenhouse Monitoring System:")
    print(f"Temperature: {temperature} °C")
    print(f"Humidity: {humidity} %")
    print("Feeding Schedule:")
    for key, value in feeding_schedule.items():
        print(f"{key}: {value}")

    # Pause for a few seconds before next reading
    time.sleep(5)