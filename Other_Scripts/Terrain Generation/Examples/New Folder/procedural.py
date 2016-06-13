"""Trying out some terrain generation via noise treated as height maps.
"""

from multiprocessing import Pool
import pygame
from noise2d import perlin




def terrain(x):
    """Interpolate the noise value and return the terrain type.
    """
    if x <-1:
        return {"name": "deep water", "color": (0, 0, 100),}
    elif -1 <= x <= -0.5:
        return {"name": "water", "color": (0, 0, 180)}
    elif -0.5 < x <= -0.3: 
        return {"name": "shallow water", "color": (0, 0, 230)}
    elif -0.3 < x <= 0.1:
        return {"name": "beach", "color": (244, 164, 96)}
    elif 0.1 < x <= 0.4:
        return {"name": "grass", "color": (127, 255, 0)}
    elif 0.4 < x <= 1:
        return {"name": "forest", "color": (0, 128, 0)}
    else:
        #x > -1
        return {"name": "deep forest", "color": (0, 50, 0)}



def gen_terrain(x, y, quadrants_wide, quadrants_tall, octaves, persistence):
    """
    x {int} Horizontal quadrant offset.
    y {int} Vertical quadrant offset.
    quadrants_wide {int} How many quadrant columns.
    quadrants_tall {int} How many quadrant rows.
    octaves and persistence {numbers} noise modifiers.
    
    returns a pygame.Surface with colorized terrain.
    """
    # v1
    #surface = pygame.Surface((quadrants_wide*quadrant_size, quadrants_tall*quadrant_size)).convert()
    # Reusable rect for space filling.
    #rect = pygame.Rect(0, 0, quadrant_size, quadrant_size)
    # Generate terrain.
    #for x in xrange(quadrant_x, quadrant_x+quadrants_wide):
        #for y in xrange(quadrant_y, quadrant_y+quadrants_tall):
            #color = terrain(perlin(x, y, octaves, persistence))["color"]
            #rect.left = x*quadrant_size
            #rect.top = y*quadrant_size
            #surface.fill(color, rect=rect)
    # Seems like I can't pickle pygame surfaces, but I can convert them to string
    # buffers and send the string back.
    #return pygame.image.tostring(surface, "RGB")
    # v2
    rowiter = xrange(x, x+quadrants_wide)
    coliter = xrange(y, y+quadrants_tall)
    return (x, y, quadrants_wide, quadrants_tall, [[terrain(perlin(row, col, octaves, persistence)) for col in coliter] for row in rowiter])



class Game(object):
    """Manage the terrain generation and the eventual display.
    """
    # How many quadrants wide and tall.
    quadrants_wide = 92
    quadrants_tall = 92
    # How big - wide and tall - is each quadrant.
    quadrant_size = 5
    # Full pixel size of the area (width, height).
    world_dims = (quadrants_wide*quadrant_size, quadrants_tall*quadrant_size)
    # Adjustments to the noise function.
    octaves = 3
    persistence = 1/100

    def __init__(self):
        # Pygame needs a few things initialized.
        pygame.init()
        self.screen = pygame.display.set_mode(self.world_dims)
                
        self.clock = pygame.time.Clock()
    
        self.background = pygame.Surface(self.world_dims).convert()

        # Loading screen.
        font = pygame.font.SysFont("arial", 18)
        text = font.render("Generating terrain...", True, (0, 0, 0))
        self.background.fill((255, 255, 255))
        self.background.blit(text, (5, 5))
    
    def run(self):
        # Start the terrain processing.
        terrain_gen_pool = Pool(processes=2)
        process_args = (0, 0, self.quadrants_wide, self.quadrants_tall, 
                        self.octaves, self.persistence)
        # Prevent beachball of waiting.
        terrain_gen_results = terrain_gen_pool.apply_async(gen_terrain, process_args)
        
        while True:
            if terrain_gen_results.ready():
                # Replace loading screen with terrain.
                # v1
                #self.background = pygame.image.fromstring(terrain_gen_results.get(), self.world_dims, "RGB")
                # v2
                offx, offy, qwide, qtall, terrain = terrain_gen_results.get()
                surface = pygame.Surface((qwide*self.quadrant_size, qtall*self.quadrant_size)).convert()
                # Reusable rect for space filling.
                rect = pygame.Rect(0, 0, self.quadrant_size, self.quadrant_size)
                # Generate terrain.
                for x, row in enumerate(terrain):
                    for y, cell in enumerate(row):
                        rect.left = x*self.quadrant_size
                        rect.top = y*self.quadrant_size
                        surface.fill(cell["color"], rect=rect)
                self.background.blit(surface, (offx,offy))
                
            self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
