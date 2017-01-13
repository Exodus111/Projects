#!/usr/bin/python3
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

class MyInputWidget(Widget):
    def __init__(self):
        super(MyInputWidget, self).__init__()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, "text")
        self.keyboard.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)
        self.input_dict = {"inf":[]}

    def check_input(self):
        if self.input_dict["inf"] != []:
            info = self.input_dict["inf"]
            self.input_dict["inf"] = []
            return info
        else:
            return None

    def on_touch_down(self, touch):
        self.input_dict["inf"] = ["MousePress", touch.x, touch.y]

    def keyboard_closed(self):
        pass

    def on_key_down(self, kb, k, txt, mod):
        self.input_dict["inf"] = ["Keydown", k, mod]

    def on_key_up(self, kb, k):
        self.input_dict["inf"] = ["Keyup", k]

class Sprite(Image):
    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)
        self.size = self.texture_size

class Player(Widget):
    def __init__(self, _input):
        super(Widget, self).__init__()
        self.walk = {"up":False, "down":False, "left":False, "right":False}
        self.input = _input
        self.sprite = Sprite(source="images/player.png")
        #self.add_widget(self.sprite)

    def w_toggle(self, inpt):
        if inpt[1][1] == "up":
            if inpt[0] == "Keydown":
                self.walk["up"] == True
            elif inpt[0] == "Keyup":
                self.walk["up"] == False
        if inpt[1][1] == "down":
            if inpt[0] == "Keydown":
                self.walk["down"] == True
            elif inpt[0] == "Keyup":
                self.walk["down"] == False
        if inpt[1][1] == "left":
            if inpt[0] == "Keydown":
                self.walk["left"] == True
            elif inpt[0] == "Keyup":
                self.walk["left"] == False
        if inpt[1][1] == "right":
            if inpt[0] == "Keydown":
                self.walk["right"] == True
            elif inpt[0] == "Keyup":
                self.walk["right"] == False
    def move(self):
        for d in self.walk:
            if self.walk[d]:
                if d == "up":
                    self.sprite.center_y += 5
                if d == "down":
                    self.sprite.center_y += -5
                if d == "left":
                    self.sprite.center_x += -5
                if d == "right":
                    self.sprite.center_x += 5


    def update(self, dt):
        inpt = self.input.check_input()
        if inpt != None:
            self.w_toggle(inpt)
        self.move()




class Background(Widget):
    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.input = None


    def update(self, dt):
        pass


class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        inputter = MyInputWidget()
        self.add_widget(inputter)
        self.player = Player(inputter)
        self.add_widget(self.player)


    def update(self, dt):
        self.player.update(dt)


class MainApp(App):
    def build(self):
        game = Game()
        Clock.schedule_interval(game.update, 1./60.)
        return game

if __name__ == "__main__":
    my_app = MainApp()
    my_app.run()
