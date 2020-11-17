from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class WindowManager(ScreenManager):
    pass
