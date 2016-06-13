class Collide(object):
    def __init__(self, walls):
        self.walls = walls
        self.bounce = False
        self.player = None
        self.perp = None
        self.xcoll_l = 1
        self.ycoll_l = 1

    def check(self, player):
        ccheck = False
        tl = tr = bl = br = False
        collided = pygame.sprite.spritecollide(player, self.walls, False)
        if collided != []:
            for brick in collided:          
                if not tl: tl = brick.rect.collidepoint(player.rect.topleft)
                if not tr: tr = brick.rect.collidepoint(player.rect.topright)
                if not bl: bl = brick.rect.collidepoint(player.rect.bottomleft)
                if not br: br = brick.rect.collidepoint(player.rect.bottomright)
            if tl and tr: # Top
                wall_vector = vec2d(10,0)
                player.dir = player.dir.projection(wall_vector)
                perp = wall_vector.perpendicular()
                perp.length = self.ycoll_l
                self.ycoll_l += 1
                player.pos += perp
                ccheck = True
            if br and bl: # Bottom
                wall_vector = vec2d(10,0)
                player.dir = player.dir.projection(wall_vector)
                perp = wall_vector.perpendicular()
                perp *= -1
                perp.length = self.ycoll_l
                self.ycoll_l += 1
                player.pos += perp
                ccheck = True
            if bl and tl: # Left
                wall_vector = vec2d(0,10)
                player.dir = player.dir.projection(wall_vector)
                perp = wall_vector.perpendicular()
                perp *= -1
                perp.length = self.xcoll_l
                self.xcoll_l += 1
                player.pos += perp
                ccheck = True
            if tr and br: # Right
                wall_vector = vec2d(0,10)
                player.dir = player.dir.projection(wall_vector)
                perp = wall_vector.perpendicular()
                perp.length = self.xcoll_l
                self.xcoll_l += 1
                player.pos += perp
                ccheck = True
            if not tl and not tr or not br and not bl:
                self.ycoll_l = 1
            if not tl and not bl or not br and not tr:
                self.xcoll_l = 1

        else:
            self.xcoll_l = 1
            self.ycoll_l = 1

        return ccheck
