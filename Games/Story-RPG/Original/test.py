#!/usr/bin/python3
from kivy.base import runTouchApp
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.core.window import Window

class HighlightLabel(Label):
    def __init__(self, **kwargs):
        super(HighlightLabel, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self._instructions = []

    def on_mouse_pos(self, *largs):
        pos = self.to_widget(*largs[1])
        if self.collide_point(*pos):
            tx, ty = pos
            tx -= self.center_x - self.texture_size[0] / 2.
            ty -= self.center_y - self.texture_size[1] / 2.
            ty = self.texture_size[1] - ty
            for uid, zones in self.refs.items():
                for zone in zones:
                    x, y, w, h = zone
                    if x <= tx <= w and y <= ty <= h:
                        self._highlight_ref(uid)
                        return
        self._clear_instructions()

    def _highlight_ref(self, name):
        if self._instructions:
            return
        store = self._instructions.append
        for box in self.refs[name]:
            box_x = self.center_x - self.texture_size[0] * 0.5 + box[0]
            box_y = self.center_y + self.texture_size[1] * 0.5 - box[1]
            box_w = box[2] - box[0]
            box_h = box[1] - box[3]
            with self.canvas:
                store(Color(0, 1, 0, 0.25))
                store(Rectangle(
                    pos=(box_x, box_y), size=(box_w, box_h)))

    def _clear_instructions(self):
        rm = self.canvas.remove
        for instr in self._instructions:
            rm(instr)
        self._instructions = []

KV = '''
HighlightLabel:
    markup: True
    text_size: self.size
    valign: 'middle'
    id: lbl
    text:
        ('[ref=headline]This is a headline![/ref] here is some'
        'more text and [ref=overview]here is an overview... '
        'Obviously this is just a test[/ref].')
'''

runTouchApp(Builder.load_string(KV))
