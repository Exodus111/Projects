from vec2d import vec2d
from load import Template, Tile
from entity import *
import pygame

class Main(Template):
    """Testing vector projection"""
    def __init__(self, size):
        super(Main, self).__init__(size)
        self.size = size
        self.background = pygame.sprite.LayeredDirty()
        self.characters = pygame.sprite.LayeredDirty()
        self.make_room(32)

        self.player = Entity()
        self.player.image = pygame.image.load("./img/blob.png")
        self.player.rect = self.player.image.get_rect()
        self.player.rect.center = (450, 500)
        self.playerpos = vec2d(self.player.rect.center)
        self.characters.add(self.player)

    # First we make a wall vector
        self.wall_vec = self.tilepos2 - self.tilepos1
    # Then we make a vector of the players direction.
        self.dir_vec = self.tilepos - self.playerpos
    # Making a vector perpendicular to the wall.
        self.perp = self.wall_vec.perpendicular()
    # Finding the endpoint of the Perpendicular vector and the players position.
        self.endpoint = self.playerpos + self.perp

    # Now we project the players direction upon the wall.
        self.proj = self.dir_vec.projection(self.wall_vec)

    # And then we make a new direction for the player.
        self.new_dir = self.playerpos + self.proj


    def make_room(self, block):
        bsize = (int(round(self.size[0] / block)), int(round(self.size[1] / block)))
        wall = "./img/wall1_medium.png"
        floor = "./img/floor1_medium.png"

        for y in range(bsize[0]):
            for x in range(bsize[1]+7):
                if y == 9 and x == 15:
                    tile = Tile(wall, (x*block,y*block))
                    self.tilepos = vec2d(tile.rect.center)
                    self.tilepos1 = vec2d(tile.rect.bottomleft)
                    self.tilepos2 = vec2d(tile.rect.topleft)
                    self.background.add(tile)
                elif x == 15:
                    tile = Tile(wall, (x*block,y*block))
                    self.background.add(tile)


    def update(self, dt):
        pass

    def draw(self):
        self.background.draw(self.screen)
        self.characters.draw(self.screen)

    # Vector between 0 and the wall. (WHITE)
        #pygame.draw.line(self.screen, (255, 255, 255), (0,0), self.tilepos.inttup(), 3)
    # Vector from 0 to Projection Vector Point. (BLUE) 
        #pygame.draw.line(self.screen, (35, 255, 255), self.proj.inttup(), (0,0), 3)
    # Vector from 0 to Player. (GREEN) 
        #pygame.draw.line(self.screen, (35, 255, 35), (0,0), self.playerpos.inttup(), 3)

    # Vector for the players direction. (PURPLE) 
        pygame.draw.line(self.screen, (255, 35, 255), self.tilepos.inttup(), self.playerpos.inttup(), 3)
    # Vector of the colliding wall. (YELLOW) 
        #pygame.draw.line(self.screen, (255, 255, 35), self.tilepos1.inttup(), self.tilepos2.inttup(), 3)
    # Vector of the players new direction. (WHITE)
        pygame.draw.line(self.screen, (255, 255, 255), self.new_dir.inttup(), self.playerpos.inttup(), 3)
    # Vector from the player to his perpendicular endpoint.
        pygame.draw.line(self.screen, (35, 255, 35), self.playerpos.inttup(), self.endpoint.inttup())





        

if __name__ == "__main__":
    s = Main((800,600))
    s.mainloop() 
