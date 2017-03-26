from kivy.config import Config

xwidth, xheight = 1024, 960
Config.set("graphics", "width", xwidth)
Config.set("graphics", "height", xheight)
Config.write()


from kivy.app import App

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock

class MyKeyboardListener(Widget):
    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed,"text")
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.keyevent = []
    
    def _keyboard_closed(self):
        print("Keyboard Closed")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "escape":
            keyboard.release()
        if keycode[1] not in self.keyevent:
            self.keyevent.append(keycode[1])

    def _on_keyboard_up(self, keyboard, keycode):
        self.keyevent.remove(keycode[1])

class MyPlayer(Widget):
    def __init__(self, **kwargs):
        super(MyPlayer, self).__init__(**kwargs)
        self.speed = 5

    def move(self, keys, walls):
        if "w" in keys:
            self.pos = [self.pos[0], self.pos[1] + self.speed]
            self.collide(walls, "w")
        if "a" in keys:
            self.pos = [self.pos[0] - self.speed, self.pos[1]]
            self.collide(walls, "a")
        if "s" in keys:
            self.pos = [self.pos[0], self.pos[1] - self.speed]
            self.collide(walls, "s")
        if "d" in keys:
            self.pos = [self.pos[0] + self.speed, self.pos[1]]
            self.collide(walls, "d")

    def collide(self, walls, key):
        for wall in walls:
            if self.collide_widget(wall):
                if key == "w":
                    self.top = wall.y - 1
                if key == "a":
                    self.x = wall.x + wall.size[0] + 1
                if key == "s":
                    self.y = wall.top + 1
                if key == "d":
                    self.x = wall.x - 1 - self.size[0]



class MyTile(Widget):
    color = ListProperty([1., 1., 1., 0.5])
    def __init__(self, wall=False, **kwargs):
        super(MyTile, self).__init__(**kwargs)

class FPSLabel(Label):
    myfps = StringProperty("")


class MyGame(Widget):
    player = ObjectProperty(None)
    keyboard = ObjectProperty(None)
    level = ObjectProperty(None)
    fps = ObjectProperty(None)

    def __init__(self):
        super(MyGame, self).__init__()
        self.delta = 0.0
        self.make_level()

    def make_level(self):
        for i in range(960):
            self.level.add_widget(MyTile())

        full_w = 1024
        full_h = 960
        box_size = 32
        color = [1., 1., 1., 1.]

        wallh_size = (full_w, box_size)
        wallv_size = (box_size, full_h - (box_size*2))
            
        wall1 = MyTile(pos=(0, full_h - box_size))
        wall1.color = color
        wall1.size = wallh_size

        wall2 = MyTile(pos=(0,0))
        wall2.color = color
        wall2.size = wallh_size

        wall3 = MyTile(pos=(0, box_size))
        wall3.color = color
        wall3.size = wallv_size

        wall4 = MyTile(pos=(full_w - box_size, box_size))
        wall4.color = color
        wall4.size = wallv_size

        wall_center = MyTile(pos=(full_w/2 - full_w/6, full_h/2 - full_h/6))
        wall_center.size = (full_w/3, full_h/3)

        self.add_widget(wall1)
        self.add_widget(wall2)
        self.add_widget(wall3)
        self.add_widget(wall4)
        self.add_widget(wall_center)
        self.walls = [wall1, wall2, wall3, wall4, wall_center]

    def update(self, dt):
        self.fps.myfps = "FPS: " + str(int(Clock.get_fps()))
        self.player.move(self.keyboard.keyevent, self.walls)

class MyApp(App):
    def build(self):
        game = MyGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MyApp().run()