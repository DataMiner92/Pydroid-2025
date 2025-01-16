import webcolors
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color

class ColorDetectorApp(App):
    def build(self):
        self.title = "Color Detector"
      
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        

        # Label to display detected color
        self.color_label = Label(text="Detected Color:", font_size=18)
        layout.add_widget(self.color_label)

        # TextInput for the hex code
        self.color_input = TextInput(hint_text="Enter Hex Code (e.g., #FF5733)", multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.color_input)

        # Button to get color name
        get_color_name_button = Button(text="Get Color Name", size_hint=(1, 0.2))
        get_color_name_button.bind(on_press=self.get_color_name)
        layout.add_widget(get_color_name_button)

        # Label to display color name
        self.color_name_label = Label(text="Color Name:", font_size=18)
        layout.add_widget(self.color_name_label)

        return layout

    def closest_color(self, requested_color):
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

    def get_color_name(self, instance):
        hex_code = self.color_input.text
        try:
            rgb = webcolors.hex_to_rgb(hex_code)
            color_name = webcolors.hex_to_name(hex_code, spec='css3')
        except ValueError:
            color_name = self.closest_color(rgb)
        self.color_name_label.text = f"Color Name: {color_name.capitalize()}"

if __name__ == '__main__':
    ColorDetectorApp().run()