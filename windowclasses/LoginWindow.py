import db_control as db
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from windowclasses import WindowManager as wm

user_info = []

class LoginWindow(Screen):
    kv = Builder.load_file("stylefolder/LoginWindow.kv")
    user_name = ObjectProperty(None)
    password = ObjectProperty(None)



    def login(self):
        user_info.append(self.user_name.text)
        user_info.append(self.password.text)

        if(db.is_user(user_info[0], user_info[1])):
            wm.screen_manager.current = "home_window"
        else:
            self.pop_up( "Invalid Login", "User Name or \n Password was incorrect.")


    def reset_inputs(self):
        self.user_name.text = ""
        self.password.text = ""


    def get_user_name(self):
        return usr_nme


    def pop_up(self, header, message):
        popup = Popup(title = header,
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400),
                      pos_hint = {"center_x": .5, "center_y": .5 })
        popup.open()
