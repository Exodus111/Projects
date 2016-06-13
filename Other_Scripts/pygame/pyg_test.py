import sys
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

def main():
    pygame.init()
    size = [500, 500]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Spinning Planet")
    clock = pygame.time.Clock()
    image = pygame.image.load("small_planet.jpg").convert()
    img_rect = image.get_rect()
    angle = 0
    done = False

    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                done = True 
        angle += 1
        if angle >= 360:
            angle = 0
        rot_image = pygame.transform.rotate(image, angle)
        rot_im_rect = rot_image.get_rect()
        rot_im_rect.center = img_rect.center
        screen.fill(BLACK)
        screen.blit(rot_image, rot_im_rect)
        pygame.display.flip()
        clock.tick(20)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()