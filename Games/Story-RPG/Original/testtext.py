#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

kv =  """
#: kivy 1.9.1

<Hello>
    size: self.size
    Label:
        size: root.size
        text: root.mytext
        font_name: './fonts/DevinneSwash.ttf'
        font_size: 25
        text_size: self.width, None
        padding_x: 50
        padding_y: 50
        pos: root.pos
        markup: True
        on_ref_press: root.clicked
"""

class Hello(Widget):
    mytext = StringProperty("""The expense of spirit in a waste of shame
Is lust in action: and till action, lust
Is perjured, murderous, bloody, full of blame,
Savage, extreme, rude, cruel, not to trust;
Enjoyed no sooner but despised straight;
Past reason hunted; and no sooner had,
Past reason hated, as a swallowed bait,
On purpose laid to make the taker mad.
Mad in pursuit and in possession so;
Had, having, and in quest to have extreme;
A bliss in proof, and proved, a very woe;
Before, a joy proposed; behind a dream.
All this the world well knows; yet none knows well
To shun the heaven that leads men to this hell.""")

    def fix_str(self):
        textlist = self.mytext.split("\n")
        textlist = [line.rstrip('\n') for line in textlist]
        text = " ".join(textlist)
        self.mytext = "[ref=click]{}[/ref]".format(text)

    def clicked(self, *args):
        print("clicked", args)

class HelloApp(App):

    def build(self):
        hello = Hello()
        hello.fix_str()
        hello.size = Window.size
        hello.center = (Window.width/2, Window.height/2)
        return hello

if __name__ == "__main__":
    Builder.load_string(kv)
    app = HelloApp()
    app.run()
