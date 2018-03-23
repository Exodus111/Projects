from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *

class DialoguePanels(FloatLayout):
    top_manager = ObjectProperty()
    bottom_manager = ObjectProperty()
    top_panel = ObjectProperty()
    bottom_panel = ObjectProperty()
    portrait = ObjectProperty()
    top_text = StringProperty()
    bottom_buttons = ListProperty()
    open_close = BooleanProperty(False)
    question_big = ObjectProperty()
    portrait = StringProperty()


    def set_size(self, size):
        self.size = size

    def add_text_to_panels(self, top_text, question_list=[]):
        self.top_text = top_text
        for n, q in enumerate(question_list):
            question = Question(question_text="{}. {}".format(n+1, q), on_touch_up=lambda x,y: self.question_selected(x, y))
            self.bottom_panel.add_widget(question)

    def clear_text(self):
        self.top_text = ""
        self.bottom_panel.clear_widgets()

    def question_menu(self, button):
        """
            Here we transition from the question buttons to a
            bigger question menu.
        """
        self.question_big.text = button.question_text
        self.bottom_manager.current = "question_big"

    def question_selected(self, button, touch=None):
        """
            This method is called when the player selects a question.
            This needs to call something in a parent widget.
        """
        if touch != None:
            if button.collide_point(*touch.pos):
                if touch.button == "right":
                    self.question_menu(button)
                elif touch.button == "left":
                    self.parent.parent.question_picked(button.question_text)    # <---Calling outside the module
        else:
            self.parent.parent.question_picked(self.question_big.text)          # <---Calling outside the module

    def drop_panels(self):
        self.open_close = not self.open_close
        if self.open_close:
            self.top_manager.current = "top_panel"
            self.bottom_manager.current = "bottom_panel"
        else:
            self.top_manager.current = "None"
            self.bottom_manager.current = "None"

class Question(Button):
    question_text = StringProperty()
    question_id = StringProperty()
