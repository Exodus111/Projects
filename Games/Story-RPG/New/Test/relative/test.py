from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.factory import Factory

class PyDemo(Factory.Widget):
    color = Factory.ListProperty([0, 0, 0, 0])

    def __init__(self, **kwargs):
        super(PyDemo, self).__init__(**kwargs)
        # Create the canvas instructions once
        with self.canvas:
            self._col = Factory.Color(rgba=self.color)
            self._rect = Factory.Rectangle(pos=self.pos, size=self.size)

        # Trigger ensures that we do not run update twice if both
        # size and pos change in same frame (quite common)
        self._trig = t = Clock.create_trigger(self._update)
        self.bind(pos=t, size=t)

    # Called automatically when color property changes; forward
    # the information to 
    def on_color(self, *largs):
        self._col.rgba = self.color

    # Called via trigger, when pos/size changes
    def _update(self, *largs):
        self._rect.pos = self.pos
        self._rect.size = self.size

runTouchApp(Builder.load_string('''
# This does [roughly] the same as the Python class
<KvDemo@Widget>:
    color: [0, 0, 0, 0]
    canvas:
        Color:
            rgba: self.color
        Rectangle:
            pos: self.pos
            size: self.size

BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        KvDemo:
            id: kvR
            color: 1, 0, 0, 1
        KvDemo:
            id: kvG
            color: 0, 1, 0, 1
        KvDemo:
            id: kvB
            color: 0, 0, 1, 1
        Button:
            text: 'Shift KvDemo'
            on_press:
                origR = kvR.color
                kvR.color = kvG.color
                kvG.color = kvB.color
                kvB.color = origR
    BoxLayout:
        PyDemo:
            id: pyR
            color: 1, 0, 0, .5
        PyDemo:
            id: pyG
            color: 0, 1, 0, .5
        PyDemo:
            id: pyB
            color: 0, 0, 1, .5
        Button:
            text: 'Shift PyDemo'
            on_press:
                origR = pyR.color
                pyR.color = pyG.color
                pyG.color = pyB.color
                pyB.color = origR
'''))