from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout


class WelcomeScreen(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.orientation = 'vertical'
        self.padding = [300, 700, 300, 700]
        self.spacing = 20
        
        self.add_widget(Label(text='Welcome to MayDay...', size_hint=(None, None), height=30, font_size=44)) 
        
        self.enter_button = Button(text='Continue', size_hint=(None, None), width=200, height=50, font_size=44)
        self.enter_button.bind(on_press=self.enter_app)
        self.add_widget(self.enter_button)
        self.spacing = 20
        
    def enter_app(self, instance):
        self.screen_manager.current = 'login'


class LoginScreen(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.orientation = 'vertical'
        self.padding = [200, 700, 200, 700]
        self.spacing = 10 

        self.add_widget(Label(text='Username', size_hint=(None, None), height=30))
        self.username = TextInput(multiline=False, size_hint=(None, None), width=400, height=70)
        self.add_widget(self.username)

        self.add_widget(Label(text='Password', size_hint=(None, None), height=30))
        self.password = TextInput(password=True, multiline=False, size_hint=(None, None), width=400, height=70)
        self.add_widget(self.password)

        self.login_button = Button(text='Login', size_hint=(None, None), width=400, height=70)
        self.login_button.bind(on_press=self.validate_login)
        self.add_widget(self.login_button)

    def validate_login(self, instance):
        username = self.username.text
        password = self.password.text
        if username == 'Admin' and password == '12345':
           
            self.screen_manager.current = 'sites'
        else:
            self.show_popup('Login Failed', 'Invalid username or password.')

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(Label(text=message))
        close_button = Button(text='Close', size_hint=(None, None), width=200, height=50)
        popup_content.add_widget(close_button)

        popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(400, 200))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class SitesScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(SitesScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [200, 800, 200, 800]
        self.spacing = 10
        self.background_color= "orange"

        self.add_widget(Label(text='Welcome, Site Page!', size_hint=(None, None), height=30))

        google_button = Button(text='Google', size_hint=(None, None), width=300, height=50)
        google_button.bind(on_press=lambda x: self.open_site('https://www.google.com'))
        self.add_widget(google_button)

        bing_button = Button(text='Bing', size_hint=(None, None), width=300, height=50)
        bing_button.bind(on_press=lambda x: self.open_site('https://www.bing.com'))
        self.add_widget(bing_button)
        
        dscience_button = Button(text='Data Science', size_hint=(None, None), width=300, height=50)
        dscience_button.bind(on_press=lambda x: self.open_site('https://www.ibm.com/topics/data-science'))
        self.add_widget(dscience_button)
        
        ai_button = Button(text='Open Lab', size_hint=(None, None), width=300, height=50)
        ai_button.bind(on_press=lambda x: self.open_site('https://www.cohere.com'))
        self.add_widget(ai_button)
        
        
        
    def close_window(App):
        screen_manager = ScreenManager(destroy)

    def open_site(self, url):
        import webbrowser
        webbrowser.open(url)

class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()

        # Welcome screen
        welcome_screen = Screen(name='welcome')
        welcome_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        welcome_layout.add_widget(WelcomeScreen(screen_manager))
        welcome_screen.add_widget(welcome_layout)
        screen_manager.add_widget(welcome_screen)

        # Login screen
        login_screen = Screen(name='login')
        login_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        login_layout.add_widget(LoginScreen(screen_manager))
        login_screen.add_widget(login_layout)
        screen_manager.add_widget(login_screen)

        # Sites screen
        sites_screen = Screen(name='sites')
        sites_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        sites_layout.add_widget(SitesScreen())
        sites_screen.add_widget(sites_layout)
        screen_manager.add_widget(sites_screen)

        screen_manager.current = 'welcome'
        return screen_manager

if __name__ == "__main__":
    MyApp().run()