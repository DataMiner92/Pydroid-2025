from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import random
import time

class TypingSpeedApp(App):
    def build(self):
        self.words = [
            "hello", "world", "python", "kivy", "typing", "speed", "test", "accuracy", 
            "apple", "banana", "orange", "grape", "watermelon", "strawberry", 
            "house", "car", "tree", "dog", "cat", "bird", "book", "pen", 
            "computer", "keyboard", "mouse", "monitor"
        ]
        self.current_word = random.choice(self.words)
        self.start_time = None
        self.end_time = None
        self.typed_words = []
        self.total_characters = 0
        self.game_started = False
        self.remaining_time = 60  # Initialize timer with 60 seconds

        layout = BoxLayout(orientation='vertical')

        # Timer Label
        self.timer_label = Label(text="Time Left: 60", font_size=34)
        layout.add_widget(self.timer_label)

        self.word_label = Label(text=f"Type: {self.current_word}", font_size=30)
        layout.add_widget(self.word_label)

        self.input_box = TextInput(multiline=False)
        self.input_box.bind(text=self.on_text_change)
        layout.add_widget(self.input_box)

        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        button_layout = BoxLayout(orientation='horizontal')
        self.start_button = Button(text="Start", background_color=(0, 1, 0, 1))  # Green
        self.reset_button = Button(text="Reset", background_color=(1, 0, 0, 1))  # Red
        self.start_button.bind(on_press=self.start_game)
        self.reset_button.bind(on_press=self.reset_game)
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.reset_button)
        layout.add_widget(button_layout)

        return layout

    def on_text_change(self, instance, value):
        if self.game_started and value.strip() == self.current_word:
            self.typed_words.append(self.current_word)
            self.total_characters += len(self.current_word)
            self.current_word = random.choice(self.words)
            self.word_label.text = f"Type: {self.current_word}"
            self.input_box.text = ""

    def update_timer(self, dt):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.text = f"Time Left: {self.remaining_time}"
        else:
            Clock.unschedule(self.update_timer)
            self.end_game(None)

    def calculate_wpm(self):
        elapsed_time = self.end_time - self.start_time
        if elapsed_time > 0:
            words_typed = len(self.typed_words)
            words_per_minute = words_typed / (elapsed_time / 60)
            return round(words_per_minute)
        return 0

    def calculate_accuracy(self):
        total_possible_characters = len(self.typed_words) * 5  # Assuming average word length is 5
        if total_possible_characters > 0:
            return (self.total_characters / total_possible_characters) * 100
        return 0

    def start_game(self, instance):
        self.game_started = True
        self.remaining_time = 60  # Reset timer
        self.start_time = time.time()
        Clock.schedule_interval(self.update_timer, 1)  # Update timer every second
        Clock.schedule_once(self.end_game, 60)  # End game after 60 seconds

    def end_game(self, dt):
        self.end_time = time.time()
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()
        self.result_label.text = f"Game Over!\nWPM: {wpm}\nAccuracy: {accuracy:.2f}%"
        self.game_started = False

    def reset_game(self, instance):
        self.current_word = random.choice(self.words)
        self.word_label.text = f"Type: {self.current_word}"
        self.input_box.text = ""
        self.result_label.text = ""
        self.timer_label.text = "Time Left: 60"
        self.start_time = None
        self.end_time = None
        self.typed_words = []
        self.total_characters = 0
        self.remaining_time = 60
        self.game_started = False
        Clock.unschedule(self.update_timer)

if __name__ == '__main__':
    TypingSpeedApp().run()