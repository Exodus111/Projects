#!/usr/bin/python3
from kivy.vector import Vector
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import StringProperty, ListProperty, BooleanProperty, ObjectProperty, NumericProperty, DictProperty
from kivy.atlas import Atlas

import random as ran

class SpeechBubble(Widget):
    """
     This class is for the speechbuble above the characters heads for comments.
     Takes info from the .kv file.
    """
    colour = ListProperty([.1, .1, .1, 0.])
    text_colour = ListProperty([.9, .9, .9, 0.])
    current_text = StringProperty("")

class NPC(Widget):
    """
     Class for each individual NPC.
    """
    frame = StringProperty(None)
    talking = BooleanProperty(False)

    def get_text_size(self, text):
        """
         Helper method, weighs the size of the text.
        """
        lab = Label(text=text, font_size=30, padding_x=5)
        lab.texture_update()
        return lab.texture_size

    def update_speech(self, text):
        """
         Used to change speech in dialogue.
        """
        if self.talking:
            tsize = self.get_text_size(text)
            anim = Animation(text_colour=[1., 1., 1., 0.], duration=.2)
            anim += Animation(size=tsize, duration=.5)
            anim.bind(on_complete=lambda x,y: self._upd_speech(text))
            anim.start(self.speech)

    def _upd_speech(self, txt):
        """
         Private helper class to update speech.
         Needed to wait for a delay after an animation.
        """
        self.speech.current_text = txt
        anim2 = Animation(text_colour=[.9, .9, .9, 1.], duration=.2)
        anim2.start(self.speech)

    def animate_speech(self, text=""):
        """
         Toggle method that will start or end a comment.
        """
        if self.speech.size[0] == 0:
            t_size = self.get_text_size(text)
            anim = Animation(colour=[.1, .1, .1, .9], duration=.2)
            anim += Animation(size=t_size, duration=.5, t='out_bounce')
            anim += Animation(text_colour=[.9, .9, .9, 1.], duration=1.)
            anim.start(self.speech)
            self.speech.current_text = text
            self.talking  = True
        else:
            anim = Animation(size=(0, 50), duration=.5, t='out_bounce')
            anim += Animation(colour=[.1, .1, .1, 0.], duration=.2)
            anim &= Animation(text_colour=[.9, .9, .9, 0.])
            anim.start(self.speech)
            self.speech.current_text = ""
            self.talking = False

class NPCController(Widget):
    """
     Controller class for all the NPCs.
    """
    npcs = ListProperty([
                    "Djonsiscus",
                    "Jarod",
                    "Tylda Travisteene",
                    "Sheila Travisteene",
                    "Mr Johes",
                    "Riff Danner"
                ])
    col_points = ListProperty([])
    def __init__(self):
        super(NPCController, self).__init__()
        x, y = (80, 250)
        for name in self.npcs:
            npc = NPC()
            npc.name = name
            w, h = npc.size
            npc.size = (w-w/4, h-h/4)
            npc.frame = 'atlas://images/{}/idle1'.format(self.gen_name(name))
            npc.pos = (x,y)
            npc.speech = SpeechBubble()
            npc.speech.pos = (npc.center_x, npc.center_y+(npc.height/2)+4)
            npc.speech.size = (0, 50)
            npc.add_widget(npc.speech)
            self.col_points.append({name:npc.center})
            x += 130
            self.add_widget(npc)

    def gen_name(self, npc):
        """
          The names of the NPCs do not correspond to what I called them.
          Probably need to remove this method.
        """
        if npc == "Djonsiscus":
            return "priest"
        elif npc == "Mr Johes":
            return "apothecary"
        elif npc == "Sheila Travisteene":
            return "girl"
        elif npc == "Tylda Travisteene":
            return "wife"
        elif npc == "Riff Danner":
            return "guy"
        elif npc == "Jarod":
            return "blacksmith"

    def update(self, dt):
        """
          Update method for the NPCs. Runs every frame.
           dt : Float. Time between frames.
        """
        pass

    def activate(self, k):
        """
          Activates a conversation.
          Not sure I need this method.
        """
        num = int(k)-1
        if num < len(self.npcs):
            self.npc_comment(self.npcs[num])
        elif num == 6:
            npc = [n for n in self.children if n.talking]
            if npc != []:
                npc = npc[0]
                npc.update_speech(ran.choice(["I mean hello!",
                                              "Uhmm, Hi?",
                                              "So, what do you want?",
                                              "Wassup?",
                                              "How YOU doin?"]))

    def comment(self, name, txt):
        """
         This makes the NPC say a comment.
        """
        npc = [n for n in self.children if n.name == name][0]
        npc.animate_speech(txt)
        anim = Animation(duration=2.)
        anim.bind(on_complete=lambda *x: npc.animate_speech())

    def coll_childs(self, w):
        return [child for child in self.children if child.collide_widget(w)]

class Player(Widget):
    """
      The player class
    """
    current_direction = StringProperty("idle")
    new_frame = BooleanProperty(True)

    def __init__(self):
        super(Player, self).__init__()
        self.new_frame = True
        self.direction = "idle"
        self.stopping = False
        self.anim_timer = 0
        self.atlas = Atlas("images/player_sheet.atlas")
        self.image = Image(allow_stretch=True, source='atlas://images/player_sheet/idle1')
        self.image.size = (64,64)
        self.size = (32,64)
        self.speech = SpeechBubble()
        self.speech.size = (0, 50)
        self.add_widget(self.speech)
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

    def get_text_size(self, text):
        """
         Helper method to measure the size of the text.
        """
        lab = Label(text=text, font_size=30, padding_x=5)
        lab.texture_update()
        return lab.texture_size

    def comment(self, text=""):
        """
          Activates the player comments.
        """
        if self.speech.size[0] == 0:
            t_size = self.get_text_size(text)
            anim = Animation(colour=[.1, .1, .1, .9], duration=.2)
            anim += Animation(size=t_size, duration=.5, t='out_bounce')
            anim += Animation(text_colour=[.9, .9, .9, 1.], duration=1.)
            anim.start(self.speech)
            self.speech.current_text = text
            self.talking  = True
            anim = Animation(duration=2.)
            anim.bind(on_complete=lambda *x: self.comment())
        else:
            anim = Animation(size=(0, 50), duration=.5, t='out_bounce')
            anim += Animation(colour=[.1, .1, .1, 0.], duration=.2)
            anim &= Animation(text_colour=[.9, .9, .9, 0.])
            anim.start(self.speech)
            self.speech.current_text = text
            self.talking = False

    def change_direction(self, d):
        """
          Helper method for the walk Animation.
        """
        if d != self.current_direction:
            self.current_direction = d
            self.new_frame = True

    def current_image(self):
        """
          Generator for the frames for the walk and idle animation.
        """
        while True:
            if self.current_direction == "idle":
                for i in range(1, 2):
                    frame = self.atlas[self.current_direction + str(i)]
                    yield frame
            else:
                for j in range(1, 5):
                    frame = self.atlas[self.current_direction + str(j)]
                    yield frame

    def keydown(self, key, mod):
        """
         Activates on Key down.
         Sets up the class variables for player walking.
        """
        if not self.stopping:
            if key[1] in ("up", "w"):
                self.moves["up"] = True
                if not self.moves["left"] and not self.moves["right"]:
                    self.change_direction("walkup")
            if key[1] in ("down", "s"):
                self.moves["down"] = True
                if not self.moves["left"] and not self.moves["right"]:
                    self.change_direction("walkdown")
            if key[1] in ("left", "a"):
                self.moves["left"] = True
                self.change_direction("walkleft")
            if key[1] in ("right", "d"):
                self.moves["right"] = True
                self.change_direction("walkright")

    def keyup(self, key):
        """
          Activates when the player releases a button.
          Removes flags on class variables that controls walking.
        """
        if not self.stopping:
            if key[1] in ("up", "w"):
                self.moves["up"] = False
            if key[1] in ("down", "s"):
                self.moves["down"] = False
            if key[1] in ("left", "a"):
                self.moves["left"] = False
                if self.moves["up"]:
                    self.change_direction("walkup")
                if self.moves["down"]:
                    self.change_direction("walkdown")
            if key[1] in ("right", "d"):
                self.moves["right"] = False
                if self.moves["up"]:
                    self.change_direction("walkup")
                if self.moves["down"]:
                    self.change_direction("walkdown")

    def set_idle(self):
        """
          Helper method for the animation, sets the player to idle.
        """
        self.moves = {i:False for i,j in self.moves.items()}
        self.change_direction("idle")

    def move(self):
        """
          Runs every frame through the update method, runs animation based on
          class variable flags.
        """
        idle = True
        for mov in self.moves:
            if self.moves[mov]:
                idle = False
                self.pos = Vector(self.pos) + Vector(self.dirs[mov])
                self.collide_objects(mov, self.parent.world.foreground.coll_childs(self))
                self.collide_objects(mov, self.parent.npcs.coll_childs(self))

        if idle:
            self.change_direction("idle")

    def update(self, dt):
        """
          Update method, runs every frame.
           dt : Float. Time between frames.
        """
        self.image.center = self.center
        if self.new_frame:
            self.frame = self.current_image()
            self.new_frame = False
        if self.anim > 10:
            self.image.texture = next(self.frame)
            self.anim = 0
        self.anim += 1
        if not self.stopping:
            self.move()
            self.collide_world()
            self.collide_npcs()
        self.speech.pos = (self.center_x, self.center_y+self.height/2+4)


    def collide_world(self):
        """
          Collision method for the world.
          Basically just does a range check, needs improvement.
        """
        if self.center[0] < 25+15: # moving west.
            self.center[0] += self.speed
        if self.center[1] < 25+30: # moving south.
            self.center[1] += self.speed
        if self.center[0] > self.world[0] - 25-15: # moving east.
            self.center[0] -= self.speed
        if self.center[1] > self.world[1] - 25-30: # moving north.
            self.center[1] -= self.speed

    def collide_objects(self, mov, collided):
        """
          Collision method for Objects in the game.
          Sends the player in the opposite direction of his current direction.
           mov : String. Direction of the player.
           collided : List. List of collided widgets.
        """
        if collided != []:
            if mov == "up":
                self.pos = Vector(self.pos) + Vector(self.dirs["down"])
            elif mov == "down":
                self.pos = Vector(self.pos) + Vector(self.dirs["up"])
            elif mov == "left":
                self.pos = Vector(self.pos) + Vector(self.dirs["right"])
            elif mov == "right":
                self.pos = Vector(self.pos) + Vector(self.dirs["left"])

    def collide_npcs(self):
        """
          Collision method that collides with NPCs.
          Reacts on widget collisions, needs improvement.
        """
        col = None
        for p in self.parent.npcs.col_points:
            for name in p:
                if Vector(self.center).distance(p[name]) <= 75:
                    col = name
                    break
            if col != None:
                break
        if col != None:
            if not self.parent.dialogue.conversation:
                self.parent.dialogue.conversation = True
                self.parent.dialogue.current_name = col
        else:
            if self.parent.dialogue.conversation:
                self.parent.dialogue.conversation = False
