#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.properties  import NumericProperty, ObjectProperty, StringProperty, ListProperty, BooleanProperty


class Menus(Widget):
    top_y = NumericProperty(0)
    bottom_y = NumericProperty(0)
    topmenu = ObjectProperty(None)
    bottommenu = ObjectProperty(None)
    toptext = StringProperty("None")
    bottomtext = ListProperty(["None", "None", "None", "None"])
    menu_on =  BooleanProperty(False)
    fade_out_top = BooleanProperty(False)
    fade_out_bottom = BooleanProperty(False)
    _counter = NumericProperty(0)

    def menusetup(self):
        self.top_y = self.size[1]
        self.bottom_y = int(-(self.size[1]/3))
        self.create_animations()

        # Creating Answer Area.
        toptext = TextArea()
        self.bind(toptext=toptext.set_text)
        self.topmenu.bind(fontcolor=toptext.set_text_color)
        self.topmenu.add_widget(toptext)

        # Creating Question area, with 4 questions.
        for _ in range(4):
            self.bottommenu.add_widget(TextArea(text="None"))

        # Binding drop menu toggle.
        self.bind(menu_on=lambda *x: self.toggle_drop_menus())

    def create_animations(self):
        # Animations for Top and bottom menues opening and closing.
        top_ypos = self.top_y - self.topmenu.height
        bottom_ypos = self.bottom_y + self.bottommenu.height
        self.top_anim_open = Animation(top_y=top_ypos, duration=.8, t="out_bounce")
        self.bottom_anim_open = Animation(bottom_y=bottom_ypos, duration=.8, t="out_bounce")
        self.top_anim_close = Animation(top_y=self.top_y+200, duration=.5, t="in_back")
        self.bottom_anim_close = Animation(bottom_y=self.bottom_y-200, duration=.5, t="in_back")

        # Animation for text fading in and out.
        self.top_text_fade_out = Animation(fontcolor=[1.,1.,1.,0.], duration=.2)
        self.top_text_fade_in = Animation(fontcolor=[1.,1.,1.,1.], duration=.2)
        self.bottom_text_fade_out = Animation(color=[1.,1.,1.,0.], duration=.2)
        self.bottom_text_fade_in = Animation(color=[1.,1.,1.,1.], duration=.2)

        self.top_text_fade_out.bind(on_complete=lambda *x: self.add_answer())
        self.bottom_text_fade_out.bind(on_complete=self.add_question)


    def update(self, dt):
        if self.fade_out_top:
            self.top_text_fade_out.start(self.topmenu)
            self.fade_out_top = False
        if self.fade_out_bottom:
            for w in self.bottommenu.children:
                self.bottommenu.bind(fontcolor=w.set_text_color)
                self.bottom_text_fade_out.start(w)
            self.fade_out_bottom = False

    def add_answer(self):
        """
          Method to add a new text in the Top Drop down menu.
          This method is run through the bind method of the fade out Animation.
          New text needs to be set in the self.toptext property, then activated
          by setting the self.fade_out_top Boolean to True.
        """
        self.toptext = self.parent.temp_text
        self.top_text_fade_in.start(self.topmenu)

    def add_question(self, _, w):
        """
          Method to add new questions to the bottom drop down menu.
          Requires that self.bottomtext (List) is updated with new Questions.
          Toggle self.fade_out_bottom to True to start this method.
        """
        w.set_text(None, self.bottomtext[self._counter])
        self.bottommenu.bind(fontcolor=w.set_text_color)
        self.bottom_text_fade_in.start(w)
        if self._counter >= 3:
            self._counter = 0
        else:
            self._counter += 1

    def toggle_drop_menus(self):
        if self.menu_on:
            self.top_anim_open.start(self)
            self.bottom_anim_open.start(self)
        else:
            self.top_anim_close.start(self)
            self.bottom_anim_close.start(self)

class BoxMenu(BoxLayout):
    fontcolor =  ListProperty([1.,1.,1.,1.])

class TextArea(Button):
    def set_text(self, obj, value):
        self.text = value

    def set_text_color(self, obj, value):
        self.color = value
