from abc import ABCMeta, abstractmethod
import pygame, sys
from pygame.locals import *
#abc means abstract base class
#Card is an abstract base class
#monster, spell, trap inherit from it

class Card(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def Mode_type():
          pass
    #Mode_type is an abstractmethod, so we can't create an instance of Card
    #

    def __init__(self, Name, funct):#, Face, Effect):
        self.Name = Name
        self.funct = funct
        #self.Face = Face
        #self.Effect = Effect
    def getMode(self,Mode):
        self.Mode = Mode

class Monster(Card):
    def __init__(self, Name, funct, Attack, Defense, Stars):
        super(self.__class__, self).__init__(Name, funct)
        #super accesses the base version of any overriden methods in a derived class
        self.Attack = Attack
        self.Defense = Defense
        self.Stars = Stars
        self.image = pygame.image.load(self.Name + ".png")
    def Mode_type(self, Mode):
        self.Mode = Mode

class Magic(Card):
    def __init__(self, Name, funct):
        super(self.__class__, self).__init__(Name, funct)
    def Mode_type(self, Mode):
        self.Mode = Mode

class Trap(Card):
    def __init__(self, Name, funct):
        super(self.__class__, self).__init__(Name, funct)
    def Mode_type(self, Mode):
        self.Mode = Mode
