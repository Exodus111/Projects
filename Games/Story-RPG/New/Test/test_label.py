from kivy.base import runTouchApp
from kivy.lang import Builder

runTouchApp(Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    Label:
        id: lbl1
        size_hint_y: None
        font_size: 28
        text: "Testing long ass line that will break up since it goes far too long!!!! Oh no, the line just keeps going and going and going and going and going!!"
        haling: "center"
        valing: "top"
        text_size: self.width, None
        height: self.texture_size[1]
    Label:
    	id: lbl2
    	size: 200, 200
    	text: "Label 2"
    Label:
    	id: lbl3
    	size: 200, 200
    	text: "Label 3"
    Label:
    	id: lbl4
    	size: 200, 200
    	text: "Label 4"
'''))