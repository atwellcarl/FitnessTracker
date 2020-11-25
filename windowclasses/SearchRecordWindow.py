import db_control as db
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from windowclasses import WindowManager as wm
from windowclasses import LoginWindow as lw

class SearchRecordWindow(Screen):
    kv = Builder.load_file("stylefolder/SearchRecordWindow.kv")
    search_word = ObjectProperty(None)
    titles = ObjectProperty(None)
    result_zero =  ObjectProperty(None)
    result_one = ObjectProperty(None)
    result_two =  ObjectProperty(None)
    result_three =  ObjectProperty(None)
    result_four =  ObjectProperty(None)

    limit = 5
    offset = 0


    def search(self):
        self.titles.text = "{:10s}   {:10s}   {:10s}   {:10s}   {:10s}".format("Name",
                     "Times Used", "Max Reps", "Max Sets", "Max Weight (lbs)")
        self.clear_labels()
        search_results = db.search_exercise_record(self.search_word.text,
                                lw.user_info[0], self.limit, self.offset)
        self.display_results(search_results)


    def return_home(self):
        self.result_zero.text = ""
        self.result_one.text = ""
        self.result_two.text = ""
        self.result_three.text = ""
        self.result_four.text = ""
        offset = 0
        wm.screen_manager.current = "home_window"


    def clear_labels(self):
        self.result_zero.text = ""
        self.result_one.text = ""
        self.result_two.text = ""
        self.result_three.text = ""
        self.result_four.text = ""


    def next(self):
        self.offset += 5
        self.search()


    def prev(self):
        if(self.offset >= 5):
            self.offset -= 5
        self.search()

    def display_results(self, search_results):
        label_num = 0
        for result in search_results:
            str_result = "{:10s}       {:10d}        {:10d}         {:10d}           {:10d}".format(result[0], result[1],
                                result[2], result[3], result[4], result[5])
            if(label_num == 0):
                self.result_zero.text = str_result
            elif(label_num == 1):
                self.result_one.text = str_result
            elif(label_num == 2):
                self.result_two.text = str_result
            elif(label_num == 3):
                self.result_three.text = str_result
            elif(label_num == 4):
                self.result_four.text = str_result
            label_num += 1
