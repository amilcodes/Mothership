import pygame
class Missiles:
    SPAWNFREQUENCY = 50
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.missilepng = None
        self.cool_down_counter = 0
        self.missilepng = pygame.image.load("finalmissile.png")#http://www.pngmart.com/image/112684
        self.mask = pygame.mask.from_surface(self.missilepng)

    def get_width(self):
        return self.missilepng.get_width()

    def get_height(self):
        return self.missilepng.get_height()

    def draw(self, screen):
        screen.blit(self.missilepng, (self.x, self.y))

    def cooldown(self):
        if self.cool_down_counter >= self.SPAWNFREQUENCY:#structure of code by Tech With Tim
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move(self, vel):
        self.x += vel
        self.SPAWNFREQUENCY -= .01