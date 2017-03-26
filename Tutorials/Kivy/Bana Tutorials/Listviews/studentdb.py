from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty

class StudentListButton(ListItemButton):
    pass

class StudentDB(BoxLayout):
    first_name_text_input = ObjectProperty()
    last_name_text_input = ObjectProperty()
    student_list = ObjectProperty()

    def submit_student(self):
        student_name = self.first_name_text_input.text + " " + self.last_name_text_input.text
        self.student_list.adapter.data.extend([student_name])
        self.student_list._trigger_reset_populate()
    def delete_student(self):
        if self.student_list.adapter.selection:
            selection = self.student_list.adapter.selection[0].text
            self.student_list.adapter.data.remove(selection)
            self.student_list._trigger_reset_populate()

    def replace_student(self):
        self.delete_student()
        self.submit_student()

class StudentDBApp(App):

    def build(self):
        return StudentDB()

dbApp = StudentDBApp()
dbApp.run()
