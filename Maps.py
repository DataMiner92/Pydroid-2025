import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarker
import requests


API_KEY = 'AIzaSyA4fiQ7ENVrQyS451czVAm_Qj0ucyTZVZ0'

class SearchScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [50, 50, 50, 50]
        self.spacing = 10

        # Search bar
        self.add_widget(Label(text='Search for a place:', size_hint=(None, None), height=30))
        self.search_input = TextInput(size_hint=(None, None), width=400, height=40)
        self.add_widget(self.search_input)

        # Search button
        self.search_button = Button(text='Search', size_hint=(None, None), width=100, height=50)
        self.search_button.bind(on_press=self.perform_search)
        self.add_widget(self.search_button)

        # MapView to display the map
        self.map_view = MapView(zoom=10, lat=0, lon=0)
        self.add_widget(self.map_view)

    def perform_search(self, instance):
        place_name = self.search_input.text
        if place_name:
            location = self.get_location(place_name)
            if location:
                self.load_map(location)

    def get_location(self, place_name):
        # Use the Google Places API to get the location
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
        params = {
            'input': place_name,
            'inputtype': 'textquery',
            'fields': 'formatted_address,name,geometry',
            'key': API_KEY
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            places_data = response.json()
            if places_data['candidates']:
                location = places_data['candidates'][0]['geometry']['location']
                return location
            else:
                return None
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Error: {err}")

    def load_map(self, location):
        lat, lng = location['lat'], location['lng']
        self.map_view.center_on(lat, lng)
        marker = MapMarker(lat=lat, lon=lng)
        self.map_view.add_marker(marker)

class MyApp(App):
    def build(self):
        return SearchScreen()

if __name__ == "__main__":
    MyApp().run()