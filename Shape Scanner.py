from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from PIL import Image as PILImage
from PIL import ImageDraw
import numpy as np
import os

class CameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Camera preview
        self.image = Image(size_hint=(1, 0.7))
        self.layout.add_widget(self.image)

        # Annotation area
        self.annotation_input = TextInput(hint_text="Enter annotation", size_hint=(1, 0.1))
        self.layout.add_widget(self.annotation_input)

        # Control buttons
        controls = BoxLayout(size_hint=(1, 0.2))
        self.capture_btn = Button(text="Capture")
        self.capture_btn.bind(on_press=self.capture_image)
        self.classify_btn = Button(text="Classify Shape")
        self.classify_btn.bind(on_press=self.classify_shape)
        controls.add_widget(self.capture_btn)
        controls.add_widget(self.classify_btn)
        self.layout.add_widget(controls)

        # Use Kivy's camera
        from kivy.uix.camera import Camera
        self.camera = Camera(play=True, resolution=(640, 480))
        self.layout.add_widget(self.camera)
        return self.layout

    def capture_image(self, instance):
        # Save the image using the Kivy camera
        self.camera.export_to_png("captured_image.png")
        self.annotation_input.text = "Image Captured!"

    def classify_shape(self, instance):
        if os.path.exists("captured_image.png"):
            # Open the image using PIL
            pil_image = PILImage.open("captured_image.png").convert("L")
            pil_image = pil_image.resize((300, 300))
            array = np.array(pil_image)
            
            # Basic shape detection logic using edges
            edges = np.where(array < 128, 1, 0)  # Simple edge detection
            
            # Count regions and classify shapes (simplistic method)
            unique, counts = np.unique(edges, return_counts=True)
            if len(unique) == 1:
                self.annotation_input.text = "No shapes detected!"
            elif len(unique) > 1:
                # Simulated classification based on pixel patterns
                if counts[1] > 50000:
                    shape = "Circle"
                elif 20000 < counts[1] <= 50000:
                    shape = "Square/Rectangle"
                else:
                    shape = "Triangle"
                self.annotation_input.text = f"Shape detected: {shape}"
        else:
            self.annotation_input.text = "Capture an image first!"

if __name__ == '__main__':
    CameraApp().run()