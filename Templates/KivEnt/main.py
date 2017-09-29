import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.properties import StringProperty

import kivent_core
from kivent_core.gameworld import GameWorld
from kivent_core.systems.position_systems import PositionSystem2D
from kivent_core.systems.renderers import Renderer
from kivent_core.managers.resource_managers import texture_manager
from kivent_core.systems.gamesystem import GameSystem

from velocity_module.velocity import VelocitySystem2D

from random import randint, choice

texture_manager.load_atlas("assets/background_objects.atlas")

class TestGame(Widget):
    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(["renderer", "position", "velocity"], callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.load_models()
        self.draw_some_stuff()

    def draw_some_stuff(self):
        init_entity = self.gameworld.init_entity
        for x in range(1000):
            pos = randint(0, Window.width), randint(0, Window.height)
            model_key = choice(["star1-4", "star1-4-2"])
            create_dict = {"position":pos,
                           "velocity": (randint(-75, 75), randint(-75, 75)),
                           "renderer":{"texture":"star1", "model_key":model_key}}
            ent = init_entity(create_dict, ["position", "velocity", "renderer"])

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle("vertex_format_4f", 7., 7., "star1", "star1-4")
        model_manager.load_textured_rectangle("vertex_format_4f", 10., 10., "star1", "star1-4-2")

    def setup_states(self):
        self.gameworld.add_state(state_name="main",
                                 systems_added=["renderer"],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=["renderer", "velocity"],
                                 screenmanager_screen="main")

    def set_state(self):
        self.gameworld.state = "main"

class DebugPanel(Widget):
    fps = StringProperty(None)
    def __init__(self, **kwargs):
        super(DebugPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.update_fps)

    def update_fps(self, dt):
        self.fps = str(int(Clock.get_fps()))
        Clock.schedule_once(self.update_fps, .05)



class BaseApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,1.)

if __name__ == "__main__":
    BaseApp().run()
