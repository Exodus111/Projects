from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class TutorialApp(App):
    def build(self):
        b = BoxLayout(orientation="vertical", padding=[50,5,50,450])
        t = TextInput(font_size=50)
        f = FloatLayout()
        s = Scatter()
        l = Label(font_size=150)

        t.bind(text=l.setter("text"))

        f.add_widget(s)
        s.add_widget(l)

        b.add_widget(f)
        b.add_widget(t)
        return b

if __name__ == "__main__":
    TutorialApp().run()