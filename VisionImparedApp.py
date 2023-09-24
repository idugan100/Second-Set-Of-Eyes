from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
import threading
from time import time
from playsound import playsound

from BackendController import Controller
controller = Controller()

class AppBoxLayout(BoxLayout):
    # Defining a variable for the last time the main button was pressed
    last_tap_time = 0

    # Defining variable that keeps track of if the program is processing
    is_processing = False

    # Defining variable that keeps track of if tutorial is playing
    is_tutorial_playing = False

    # Need dt because Clock.schedule_one() automatically passed dt
    # argument
    def on_button_hold(self, dt=None):
        if self.is_tutorial_playing:
            print("End tutorial")

        else:
            threading.Thread(target=self.playingTutorial).start()

    def playingTutorial(self):
        self.is_tutorial_playing = True

        playsound("Assets/Sounds/tutorial_1.mp4")
        playsound("Assets/Sounds/tutorial_2.mp4")

        self.is_tutorial_playing = False

    def on_button_press(self):
        if self.is_processing:
            return

        else:
            # Schedule an event for button being held
            self.hold_event = Clock.schedule_once(self.on_button_hold, 1.5)

            # Checking if the last time the main button was pressed was less than .5 seconds
            # ago
            current_time = time()
            if current_time - self.last_tap_time < .5 and self.last_tap_time != 0:
                self.hold_event.cancel()

                # Starting the BackendController in a different thread
                threading.Thread(target=controller.takingPictureToSpeech).start()

                # Setting the processing flag
                self.is_processing = True

                # Scheduling the audible processing message
                self.event = Clock.schedule_interval(self.processing, 1)

                self.last_tap_time = current_time

            else:
                self.last_tap_time = current_time

# Canceling the event scheduled to happen on button hold
    def on_button_release(self):
        self.hold_event.cancel()

    # Plays processing on a different thread than the image captioning api
    # so that a loading noise can be played
    # Need dt because Clock.schedule_one() automatically passed dt
    # argument
    def processing(self, dt=None):
        if controller.checkFinished() == False:
            playsound("Assets/Sounds/processing.mp4")

        else:
            self.event.cancel()
            controller.setFinishedFalse()

            # Setting the processing flag
            self.is_processing = False

class Application(App):
    def build(self):
        Builder.load_file("visionimpared.kv")
        return AppBoxLayout()

    def on_start(self):
        threading.Thread(target=self.welcomeMessage).start()

    # Need dt because Clock.schedule_one() automatically passed dt
    # argument
    def welcomeMessage(self, dt=None):
        # Playing welcome message on app boot
        playsound("Assets/Sounds/welcome.mp4")