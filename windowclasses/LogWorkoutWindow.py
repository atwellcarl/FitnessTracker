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
        global exercises
        h = 0
        m = 0
        try:
            h = int(self.hours.text)
            m = int(self.minutes.text)
            workout_id = db.create_workout(self.spinner.text, h, m)
            # create relation between user and new workout
            db.create_has_workout(lw.user_info[0], workout_id, self.time.tm_mon,
                        self.time.tm_mday, self.time.tm_year)
            # for each exercise create a completed exercise relation
            for exercise in exercises:
                # check if exercise is in table
                if(not db.contains_exercise(exercise["exercise_name"])):
                    self.pop_up("Error Exercise Not Found", "The exercise : {} could not be found"
                            .format(exercise["exercise_name"]))
                else:
                    db.create_completed_exercise(exercise["exercise_name"], workout_id,
                    exercise["reps"], exercise["sets"], exercise["weight"])
                    records = db.get_exercise_record(lw.user_info[0], exercise["exercise_name"])
                    update_records = [1] * 3

                    # if records are null then create new record for exercise
                    if(records == None):
                        db.create_exercise_record(lw.user_info[0], exercise["exercise_name"],
                        exercise["reps"], exercise["sets"], exercise["weight"], 1)
                    else:
                        if(records[0] < int(exercise["reps"])):
                            update_records[0] = int(exercise["reps"])
                        else:
                            update_records[0] = records[0]

                        if(records[1] < int(exercise["sets"])):
                            update_records[1] = int(exercise["sets"])
                        else:
                            update_records[1] = records[1]

                        if(records[2] < int(exercise["weight"])):
                            update_records[2] = int(exercise["weight"])
                        else:
                            update_records[2] = records[2]

                        db.update_records(records[4], update_records[0],
                                          update_records[1], update_records[2], int(records[3]) + 1)

            # clear out structures and return to home page
            exercises = []
            self.hours.text = "Hrs"
            self.minutes.text = "Min"
            self.pop_up("Success!", "Your Workout Has Been Logged!")
            wm.screen_manager.current = "home_window"
        except Exception as e:
            self.pop_up("Error", "Please enter the length of your workout")



    def log_exercise(self):
        exercise = {}
        exercise["exercise_name"] = self.exercise_name.text
        exercise["reps"] = self.reps.text
        exercise["sets"] = self.sets.text
        exercise["weight"] = self.weight.text
        if(db.contains_exercise(exercise["exercise_name"])):
            self.pop_up("Logged Exercise", "Exercise has been logged.\n Add Another Exercise or Log the Workout.")

            # reset inputs
            self.exercise_name.text = ""
            self.reps.text = ""
            self.sets.text = ""
            self.weight.text = ""
            exercises.append(exercise)
        else:
            self.pop_up("Error Exercise Not Found", "The exercise : {} could not be found"
                    .format(exercise["exercise_name"]))


    def return_home(self):
        self.exercise_name.text = ""
        self.reps.text = ""
        self.sets.text = ""
        self.weight.text = ""
        wm.screen_manager.current = "home_window"



    def pop_up(self, header, message):
        popup = Popup(title = header,
                      content = Label(text = message),
                      size_hint = (None, None), size = (800, 800),
                      pos_hint = {"center_x": .5, "center_y": .5 })
        popup.open()
