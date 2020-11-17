import db_control as db
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from windowclasses import WindowManager as wm
from windowclasses import LoginWindow as lw
import time

exercises = []

class LogWorkoutWindow(Screen):
    kv = Builder.load_file("stylefolder/LogWorkoutWindow.kv")
    time = time.localtime(time.time())

    spinner = ObjectProperty(None)
    hours = ObjectProperty(None)
    minutes = ObjectProperty(None)
    exercise_name = ObjectProperty(None)
    reps = ObjectProperty(None)
    sets = ObjectProperty(None)
    weight = ObjectProperty(None)


    def create_workout(self):
        workout_id = db.create_workout(self.spinner.text, self.hours.text, self.minutes.text)
        # create relation between user and new workout
        db.create_has_workout(lw.user_info[0], workout_id, self.time.tm_mon,
                    self.time.tm_mday, self.time.tm_year)


    def log_exercise(self):
        exercise = {}
        exercise["exercise_name"] = self.exercise_name.text
        exercise["reps"] = self.reps.text
        exercise["sets"] = self.sets.text
        exercise["weight"] = self.weight.text

        self.pop_up("Logged Exercise", "Exercise has been logged.\n Add Another Exercise or Log the Workout.")

        # reset inputs
        self.exercise_name.text = ""
        self.reps.text = ""
        self.sets.text = ""
        self.weight.text = ""
        exercises.append(exercise)
        print(exercises)


    def pop_up(self, header, message):
        popup = Popup(title = header,
                      content = Label(text = message),
                      size_hint = (None, None), size = (800, 800),
                      pos_hint = {"center_x": .5, "center_y": .5 })
        popup.open()
