import webcolors
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from PIL import Image

class ColorScannerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Label to display detected color
        self.color_label = Label(text="Detected Color: None", font_size=32)
        layout.add_widget(self.color_label)

        # FileChooser to select an image file
        self.file_chooser = FileChooserListView(size_hint=(1, 0.7))
        layout.add_widget(self.file_chooser)

        # "Select" button to confirm selection
        select_button = Button(text="Select", size_hint=(1, 0.1))
        select_button.bind(on_press=self.on_select)
        layout.add_widget(select_button)

        return layout

    def on_select(self, instance):
        selection = self.file_chooser.selection
        if selection:
            file_path = selection[0]
            color_hex = self.detect_color(file_path)
            color_name = self.get_color_name(color_hex)
            self.color_label.text = f"Detected Color: {color_name} ({color_hex})"

    def detect_color(self, file_path):
        # Open the image file
        img = Image.open(file_path)
        
        # Resize the image to speed up processing
        img = img.resize((50, 50), Image.LANCZOS)
        
        # Get the most common color
        img_colors = img.getcolors(50 * 50)
        most_frequent_color = max(img_colors, key=lambda x: x[0])[1]
        
        # Convert RGB to hexadecimal
        color_hex = "#{:02x}{:02x}{:02x}".format(*most_frequent_color)
        return color_hex

    def closest_color(self, requested_color):
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

    def get_color_name(self, hex_code):
        try:
            rgb = webcolors.hex_to_rgb(hex_code)
            color_name = webcolors.hex_to_name(hex_code, spec='css3')
        except ValueError:
            color_name = self.closest_color(rgb)
        return color_name.capitalize()

if __name__ == "__main__":
    ColorScannerApp().run()