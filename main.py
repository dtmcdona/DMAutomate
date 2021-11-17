import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.0')

class MyRoot(BoxLayout):

    def __init__(self):
        super(MyRoot, self).__init__()

    def record_macro(self):
        self.status.text = "Recording..."

    def play_macro(self):
        self.status.text = "Playing"

    def load_macro(self):
        self.status.text = "Loading"

class DMAutomate(App):

    def build(self):
        return MyRoot()

dmAutomate = DMAutomate()
dmAutomate.run()