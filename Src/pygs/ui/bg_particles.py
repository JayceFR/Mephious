import pygame
import math
import random
from pygame.locals import *

class Master():
    def __init__(self, img) -> None:
        self.particles = []
        self.particle_generation_cooldown = 200
        self.particle_generation_last_update = 0
        self.img = img

    def add_particles(self):
        self.particles.append(Particles(random.randint(-100,6000)//2, random.randint(-50,50)//2, 5, self.img))

    def recursive_call(self, time, display, scroll, dt):
        if self.particles != []:
            for pos, particle in sorted(enumerate(self.particles), reverse=True):
                particle.move(time, dt)
                particle.draw(display, scroll)
                if not particle.alive:
                    self.particles.pop(pos)
        if time - self.particle_generation_last_update > self.particle_generation_cooldown:
            self.particle_generation_last_update = time
            self.add_particles()


class Particles():
    def __init__(self, x, y, speed, imgs) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.imgs = imgs
        self.img = imgs[random.randint(0,1)]
        self.current_img = self.img
        self.gravity = 5
        self.alive = True
        self.angle = random.randint(0,360)
        self.angle_change_cooldown = 100
        self.angel_change_last_update = 0
        self.radius = 1.5

    def move(self, time, dt):
        if time - self.angel_change_last_update > self.angle_change_cooldown:
            self.angel_change_last_update = time
            self.angle += random.randint(0,10)
            if self.angle > 360:
                self.angle = 0
        self.x += math.sin(math.radians(self.angle)) * dt
        self.y += 0.5 * dt
        if self.x > 10000 or self.y > 1200:
            self.alive = False

    def draw(self, display, scroll):
        '''pygame.draw.circle(display, (155, 50, 50), (self.x - scroll[0], self.y - scroll[1]), self.radius)
        self.radius *= 2
        display.blit(self.circle_surf(), (int(self.x- self.radius) - scroll[0], int(self.y - self.radius) - scroll[1]), special_flags=BLEND_RGBA_ADD)
        self.radius /= 2'''
        self.current_img = self.img.copy()
        self.current_img = pygame.transform.rotate(self.current_img, self.angle)
        display.blit(self.current_img, (self.x - scroll[0], self.y - scroll[1]))

    def circle_surf(self):
        surf = pygame.Surface((self.radius * 4, self.radius * 4))
        pygame.draw.circle(surf, (20, 20, 20), (self.radius, self.radius), self.radius)
        surf.set_colorkey((0, 0, 0))
        return surf
