#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.atlas import Atlas

class TestApp(App):

    def build(self):
        label = Label(text="Testing going on.")
        atlas = Atlas("player_sheet.atlas")
        image1 = Image(allow_stretch=True)
        image1.texture = atlas["walkleft4"]
        label.add_widget(image1)
        return label

if __name__ == "__main__":
    app = TestApp()
    app.run()

"""
    def load_atlas(self, *atlas):
        self.idle = []
        self.walkdown = []
        self.walkleft = []
        self.walkright = []
        self.walkup = []
        for img in atlas:
            if "idle" in img:
                self.idle.append(img)
            elif "walkdown" in img:
                self.walkdown.append(img)
            elif "walkleft" in img:
                self.walkleft.append(img)
            elif "walkright" in img:
                self.walkright.append(img)
            elif "walkup" in img:
                self.walkup.append(img)

    def change_direction(self, d):
        if d != self.direction:
            if d == "stop":
                self.cur_imgs = self.idle
            elif d == "down":
                self.cur_imgs = self.walkdown
            elif d == "left":
                self.cur_imgs = self.walkleft
            elif d == "right":
                self.cur_imgs = self.walkright
            elif d == "up":
                self.cur_imgs = self.walkup
            self.direction = d
            self.new_frame = True


                    'atlas://images/player_imgs/idle1', 'atlas://images/player_imgs/idle2',
                    'atlas://images/player_imgs/walkdown1', 'atlas://images/player_imgs/walkdown2',
                    'atlas://images/player_imgs/walkdown3', 'atlas://images/player_imgs/walkdown4',
                    'atlas://images/player_imgs/walkleft1', 'atlas://images/player_imgs/walkleft2',
                    'atlas://images/player_imgs/walkleft3', 'atlas://images/player_imgs/walkleft4',
                    'atlas://images/player_imgs/walkright1', 'atlas://images/player_imgs/walkright2',
                    'atlas://images/player_imgs/walkright3', 'atlas://images/player_imgs/walkright4',
                    'atlas://images/player_imgs/walkup1', 'atlas://images/player_imgs/walkup2',
                    'atlas://images/player_imgs/walkup3', 'atlas://images/player_imgs/walkup4'

"""
