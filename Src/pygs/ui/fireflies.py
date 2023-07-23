import pygame
import random
import math
from pygame.locals import *
class FireFly():
    def __init__(self, x, y, radius) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = random.randint(0,360)
        self.angle_change_cooldown = 100
        self.angel_change_last_update = 0
    
    def move(self, time):
        if time - self.angel_change_last_update > self.angle_change_cooldown:
            self.angel_change_last_update = time
            self.angle += random.randint(0,10)
            if self.angle > 360:
                self.angle = 0
        self.x += math.cos(math.radians(self.angle)) * 0.5
        self.y += math.sin(math.radians(self.angle)) * 0.5
    
    def draw(self, display, scroll):
        #pygame.draw.circle(display, (255, 255, 255), (self.x - scroll[0], self.y - scroll[1]), self.radius)
        display.draw_circle((255,255,255), (self.x - scroll[0], self.y - scroll[1]), self.radius, ui_display = False)
        self.radius *= 8
        display.blit(self.circle_surf(), (int(self.x- self.radius) - scroll[0], int(self.y - self.radius) - scroll[1]), special_flag=BLEND_RGBA_ADD, ui_display = False)
        self.radius /= 8
    
    def circle_surf(self):
        surf = pygame.Surface((self.radius * 4, self.radius * 4))
        pygame.draw.circle(surf, (0, 0, 50), (self.radius, self.radius), self.radius)
        surf.set_colorkey((0, 0, 0))
        surf.set_colorkey((0,0,0))
        return surf
    

class Fireflies():
    def __init__(self, x, y, width_of_entire_game, height_of_entire_game) -> None:
        self.x = x 
        self.y = y
        self.width_of_entire_game = width_of_entire_game * 2
        self.height_of_entire_game = height_of_entire_game * 2 
        self.fireflies = []
        for x in range(150):
            self.fireflies.append(FireFly(random.randint(-100,self.width_of_entire_game)//2, random.randint(-100,self.height_of_entire_game)//2, 2))
            
    def recursive_call(self, time, display, scroll):
        for firefly in self.fireflies:
            firefly.move(time)
            firefly.draw(display, scroll)
