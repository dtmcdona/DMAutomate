from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class DMAutomate(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.8)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.add_widget(Image(source="logo.png"))
        self.title = Label(text="DMAutomate")
        self.window.add_widget(self.title)
        self.status = Label(text="Standby")
        self.window.add_widget(self.status)
        self.record = Button(text="Start Recording")
        self.record.bind(on_press=self.record_callback)
        self.window.add_widget(self.record)

        return self.window

    def record_callback(self, instance):
        self.status.text = "Recording"

if __name__ == "__main__":
    DMAutomate().run()