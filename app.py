from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class DMAutomate(App):
    def build(self):
        self.is_recording = False
        self.window = BoxLayout(orientation ='vertical')
        self.toolbar = BoxLayout(orientation ='horizontal', size_hint = (1, .1))
        self.statusbar = BoxLayout(orientation ='horizontal', size_hint = (1, .1))
        self.bodysection = BoxLayout(orientation='vertical')
        self.record = Button(text="Record")
        self.create = Button(text="Create")
        self.open = Button(text="Open")
        self.save = Button(text="Save")
        self.delete = Button(text="Delete")
        self.appsettings = Button(text="Settings")
        self.play = Button(text="Play", size_hint = (.2, 1))
        self.currentfile = "dm_macro.py"
        self.status = "Standby"
        self.duration = ""
        self.statusbartext = Button(text="Current file: " + self.currentfile +
                                         " - Status: " + self.status +
                                         " - Duration: " + self.duration)
        self.record.bind(on_press=self.record_callback)
        self.toolbar.add_widget(self.record)
        self.toolbar.add_widget(self.create)
        self.toolbar.add_widget(self.open)
        self.toolbar.add_widget(self.delete)
        self.toolbar.add_widget(self.save)
        self.toolbar.add_widget(self.appsettings)
        self.statusbar.add_widget(self.play)
        self.statusbar.add_widget(self.statusbartext)
        self.window.add_widget(self.toolbar)
        self.window.add_widget(self.statusbar)
        self.window.add_widget(self.bodysection)

        return self.window

    def record_callback(self, instance):
        self.is_recording = False if self.is_recording else True
        self.record.text = "Stop" if self.is_recording else"Record"
        self.status = "Recording" if self.is_recording else "Standby"
        self.update_status_bar()

    def update_status_bar(self):
        self.statusbartext.text = "Current file: " + self.currentfile + \
                                    " - Status: " + self.status + \
                                    " - Duration: " + self.duration

if __name__ == "__main__":
    DMAutomate().run()