#!/usr/bin/python3
from kivy.app import App
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, BoundedNumericProperty
from kivy.atlas import Atlas

class EventHandler(Widget):
    def __init__(self):
        super(EventHandler, self).__init__()
        self.calls = {
            "keydown":None,
            "keyup":None
        }
        self.keyboard = Window.request_keyboard(self.key_off, self)
        self.keyboard.bind(on_key_down=self.key_down)
        self.keyboard.bind(on_key_up=self.key_up)

    def key_up(self, k, keycode):
        self.calls["keyup"](keycode)

    def key_down(self, keyboard, keycode, text, mod):
        self.calls["keydown"](keycode, mod)

    def key_off(self):
        pass

class Sprite(Widget):
    current_direction = StringProperty("idle")
    new_frame = BooleanProperty(True)
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.new_frame = True
        self.direction = "idle"
        self.anim_timer = 0

    def change_direction(self, d):
        if d != self.current_direction:
            self.current_direction = d
            self.new_frame = True

    def current_image(self):
        while True:
            if self.current_direction == "idle":
                for i in range(1, 2):
                    frame = self.atlas[self.current_direction + str(i)]
                    yield frame
            else:
                for j in range(1, 5):
                    frame = self.atlas[self.current_direction + str(j)]
                    yield frame

class Player(Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.atlas = Atlas("images/player_sheet.atlas")
        self.image = Image(allow_stretch=True, source='atlas://images/player_sheet/idle1')
        self.image.size = (64,64)
        self.size = (32,64)
        self.add_widget(self.image)
        self.target = [0,0]
        self.speed = 3
        self.anim = 0
        self.world = (0,0)
        self.moves = {"up":False, "down":False, "left":False, "right":False}
        self.dirs = {
        "up":(0, self.speed),
        "down":(0, -self.speed),
        "left":(-self.speed, 0),
        "right":(self.speed, 0)
        }

    def keydown(self, key, mod):
        if key[1] in ("up", "w"):
            self.moves["up"] = True
            if not self.moves["left"] or not self.moves["right"]:
                self.change_direction("walkup")
        if key[1] in ("down", "s"):
            self.moves["down"] = True
            if not self.moves["left"] or not self.moves["right"]:
                self.change_direction("walkdown")
        if key[1] in ("left", "a"):
            self.moves["left"] = True
            self.change_direction("walkleft")
        if key[1] in ("right", "d"):
            self.moves["right"] = True
            self.change_direction("walkright")

    def keyup(self, key):
        if key[1] in ("up", "w"):
            self.moves["up"] = False
        if key[1] in ("down", "s"):
            self.moves["down"] = False
        if key[1] in ("left", "a"):
            self.moves["left"] = False
        if key[1] in ("right", "d"):
            self.moves["right"] = False

    def move(self):
        idle = True
        for mov in self.moves:
            if self.moves[mov]:
                idle = False
                self.pos = Vector(self.pos) + Vector(self.dirs[mov])
        if idle:
            self.change_direction("idle")

    def update(self, dt):
        self.image.center = self.center
        if self.new_frame:
            self.frame = self.current_image()
            self.new_frame = False
        if self.anim > 10:
            self.image.texture = next(self.frame)
            self.anim = 0
        self.anim += 1
        self.move()
        self.collide_world()
        self.collide_objects()


    def collide_world(self):
        if self.center[0] < 25+15: # moving west.
            self.center[0] += self.speed
        if self.center[1] < 25+30: # moving south.
            self.center[1] += self.speed
        if self.center[0] > self.world[0] - 25-15: # moving east.
            self.center[0] -= self.speed
        if self.center[1] > self.world[1] - 25-30: # moving north.
            self.center[1] -= self.speed

    def _project(self, b):
        b_length_squared = b[0]*b[0]+b[1]*b[1]
        projected_length = Vector(self.pos).dot(b)
        return Vector(b)*(projected_length/b_length_squared)

    def collide_objects(self):
        collided = self.parent.world.foreground.coll_childs(self)
        if collided != []:
            return True
        else:
            return False


class GameWorld(Widget):
    def __init__(self, **kwargs):
        super(GameWorld, self).__init__(**kwargs)
        self.background = Image(source='images/game_borders.png', size=(2048/2,1080/2))
        self.size = self.background.size
        self.add_widget(self.background)
        self.foreground = ForeGround(size=self.size)
        self.foreground.add_widget(Clutter(img='images/obj_32px.png', pos=(100, 200)))
        self.foreground.add_widget(Clutter(img='images/obj_128x32px.png', pos=(200, 200)))
        self.foreground.add_widget(Clutter(img='images/obj_64px.png', pos=(100, 400)))
        self.add_widget(self.foreground)



    def update(self, dt):
        self.foreground.update(dt)

class ForeGround(Widget):
    def coll_childs(self, w):
        return [child for child in self.children if child.collide_widget(w)]

    def update(self, dt):
        for child in self.children:
            child.update(dt)

class Clutter(Widget):
    def __init__(self, img, pos):
        super(Clutter, self).__init__()
        self.image = Image(source=img)
        self.size = self.image.size = self.image.texture_size
        self.pos = pos
        self.image.center = self.center
        self.add_widget(self.image)

    def update(self, dt):
        pass

class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.event = EventHandler()
        self.player = Player()
        self.player.center = Window.center
        self.event.calls["keyup"] = self.player.keyup
        self.event.calls["keydown"] = self.player.keydown
        self.world = GameWorld()
        Window.size = self.world.size
        self.player.world = self.world.size
        self.add_widget(self.event)
        self.add_widget(self.world)
        self.add_widget(self.player)

    def update(self, dt):
        self.world.update(dt)
        self.player.update(dt)


class MainApp(App):
    def build(self):
        game = Game()
        Clock.schedule_interval(game.update, 1./60.)
        return game

if __name__ == "__main__":
    my_app = MainApp()
    my_app.run()
