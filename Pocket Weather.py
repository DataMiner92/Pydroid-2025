from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color
import requests

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

class WeatherApp(App):
    def build(self):
        self.title = "Weather App"

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Background color using Canvas
        with layout.canvas.before:
            Color(1, 1, 0.1, 1)  # Orange color
            self.rect = Rectangle(size=(layout.width, layout.height), pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        city_label = Label(text="Pocket Weather App:", font_size=38, color=(0, 0, 0, 1))
        layout.add_widget(city_label)
        
        detail_label = Label(text="Get Weather Update-  City to City", font_size=22, color=(0, 0, 0, 1))
        layout.add_widget(detail_label)

        self.city_input = TextInput(hint_text="City Name", multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.city_input)

        search_button = Button(text="Get Weather", size_hint=(1, 0.2), background_color=(1, 0.5, 0, 1))
        search_button.bind(on_press=self.show_weather)
        layout.add_widget(search_button)

        self.weather_label = Label(text="", halign='center', valign='middle', font_size=56, color=(0, 0, 0, 1))
        self.weather_label.bind(size=self.weather_label.setter('text_size'))
        layout.add_widget(self.weather_label)

        return layout

    def show_weather(self, instance):
        city_name = self.city_input.text
        if city_name:
            weather_info = get_weather(city_name)
            self.weather_label.text = weather_info
        else:
            popup = Popup(title='Input Error', content=Label(text='Please enter a city name'),
                          size_hint=(0.6, 0.4))
            popup.open()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    WeatherApp().run()