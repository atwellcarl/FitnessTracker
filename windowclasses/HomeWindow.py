import db_control as db
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from windowclasses import WindowManager as wm

class HomeWindow(Screen):
    kv = Builder.load_file("stylefolder/HomeWindow.kv")

    def log_workout(self):
        wm.screen_manager.current = "log_workout_window"
