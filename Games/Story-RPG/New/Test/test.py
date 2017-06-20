from kivy.base import runTouchApp
from kivy.factory import Factory
from kivy.core.image import Image as CoreImage

class Aligned(Factory.Widget):
    def __init__(self, **kwargs):
        super(Aligned, self).__init__(**kwargs)
        fg = CoreImage("imgs/foreground.png").texture
        bg = CoreImage("imgs/background.png").texture
        fg_size = (fg.size[0]*2, fg.size[1]*2)
        bg_size = (bg.size[0]*2, bg.size[1]*2)
        with self.canvas:
            Factory.Rectangle(size=fg_size, texture=fg, pos=(0, 0))
            Factory.Rectangle(size=bg_size, texture=bg, pos=(0, 1))

runTouchApp(Aligned())
