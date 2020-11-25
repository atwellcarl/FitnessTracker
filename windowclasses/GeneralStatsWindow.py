import db_control as db
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from windowclasses import WindowManager as wm
from windowclasses import LoginWindow as lw
import time

class GeneralStatsWindow(Screen):
    kv = Builder.load_file("stylefolder/GeneralStatsWindow.kv")
    time = time.localtime(time.time())

    fav_exercise = ObjectProperty(None)
    total_hours = ObjectProperty(None)
    percentage = ObjectProperty(None)
    type_counts = ObjectProperty(None)


    def get_personal_stats(self):
        fav_ex_query = db.get_fav_exercise(lw.user_info[0])
        self.fav_exercise.text = "Favorite Exercise is {} used {} times.".format(fav_ex_query[1], fav_ex_query[0])

        total_hours = db.get_hours_workedout(lw.user_info[0], self.time.tm_mon)[0]

        self.total_hours.text = "Total Workout Hours This Month: {}".format(total_hours)

        percentage = db.get_tot_app_percentage(self.time.tm_mon, lw.user_info[0])[0]
        self.percentage.text = "Cross user monthly workout percentage {}".format(round(percentage, 2))

        type_counts = db.get_workout_type_count(lw.user_info[0])
        str = "Youre Workout Type Counts \n"
        for tuple in type_counts:
            str += "    {}: {}\n".format(tuple[0], tuple[1])
        self.type_counts.text = str



    def return_home(self):
        wm.screen_manager.current = "home_window"
