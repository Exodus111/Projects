#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as KImage
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.clock import Clock

from PIL import Image
import numpy as np

class Main(Widget):

    def setup(self):
        fg_image = Image.open("imgs/foreground.png")
        fg_size = fg_image.size
        fg_size = (fg_size[0]*3, fg_size[1]*3)
        fg_image = fg_image.resize(fg_size)

        #arr1 = np.fromstring(fg_image.tobytes(), np.uint8)
        fg = Texture.create(size=fg_size)
        fg.blit_buffer(fg_image.tobytes(), colorfmt="rgba", bufferfmt="ubyte")

        #fg_image.save("imgs/fg.png")
        #fg = KImage(source="imgs/fg.png").texture

        bg_image = Image.open("imgs/background.png")
        bg_size = bg_image.size
        bg_size = (bg_size[0]*3, bg_size[1]*3)
        bg_image = bg_image.resize(bg_size)

        #arr2 = np.fromstring(bg_image.tobytes(), np.uint8)
        bg = Texture.create(size=bg_size)
        bg.blit_buffer(bg_image.tobytes(), colorfmt="rgba", bufferfmt="ubyte")

        #bg_image.save("imgs/bg.png")
        #bg = KImage(source="imgs/bg.png").texture

        with self.canvas:
            Rectangle(texture=bg, pos=[-200, -400], size=bg.size)
            Rectangle(texture=fg, pos=[-200, -400], size=fg.size)

    def update(self, dt):
        pass

class ImageCheckApp(App):
    def build(self):
        game = Main()
        game.setup()
        Clock.schedule_interval(game.update, 1/60)
        return game

if __name__ == "__main__":
    app = ImageCheckApp()
    app.run()
