from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from time import time

from BackendController import Controller
controller = Controller()

class AppBoxLayout(BoxLayout):
    # Defining a variable for the last time the main button was pressed
    last_tap_time = 0

    # Need dt because Clock.schedule_one() automatically passed dt
    # argument
    def on_button_hold(self, dt=None):
        print("Tutorial")

    def on_button_press(self):
        # Schedule an event for button being held
        self.hold_event = Clock.schedule_once(self.on_button_hold, 1.5)

        # Checking if the last time the main button was pressed was less than .5 seconds
        # ago
        current_time = time()
        if current_time - self.last_tap_time < .5 and self.last_tap_time != 0:
            self.hold_event.cancel()

            controller.takingPictureToSpeech()

            self.last_tap_time = current_time
        else:
            self.last_tap_time = current_time

# Canceling the event scheduled to happen on button hold
    def on_button_release(self):
        self.hold_event.cancel()

class Application(App):
    def build(self):
        Builder.load_file("visionimpared.kv")
        return AppBoxLayout()