from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

class StopwatchApp(App):
    def build(self):
        self.elapsed_time = 0
        self.running = False

        # Layout
        layout = BoxLayout(orientation='vertical')

        # Label to display time
        self.time_label = Label(text="0.0.0", font_size=72)
        layout.add_widget(self.time_label)

        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.3))

        start_btn = Button(text="Start", on_press=self.start)
        stop_btn = Button(text="Stop", on_press=self.stop)
        reset_btn = Button(text="Reset", on_press=self.reset)

        btn_layout.add_widget(start_btn)
        btn_layout.add_widget(stop_btn)
        btn_layout.add_widget(reset_btn)

        layout.add_widget(btn_layout)

        return layout

    def update_time(self, dt):
        if self.running:
            self.elapsed_time += dt
            self.time_label.text = str(round(self.elapsed_time, 1))

    def start(self, instance):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update_time, 0.1)

    def stop(self, instance):
        self.running = False
        Clock.unschedule(self.update_time)

    def reset(self, instance):
        self.running = False
        self.elapsed_time = 0
        self.time_label.text = "00.00.00"
        Clock.unschedule(self.update_time)

if __name__ == "__main__":
    StopwatchApp().run()