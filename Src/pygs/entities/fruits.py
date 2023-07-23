import pygame
import Src.pygs.utils.physics as physics

class Fruits(physics.PhysicsEntity):
    def __init__(self, loc, animation) -> None:
        super().__init__(loc, animation[0].get_width(), animation[0].get_height())
        self.animation = animation
        self.movement = [0,0]
        self.collision_type = {}
        self.frame = 0
        self.frame_last_update = 0 
        self.frame_cooldown = 200
        self.display_x = 0
        self.display_y = 0
        self.facing_right = True
    
    def move(self, time, tiles, player_x):
        self.movement = [0,0]
        self.movement[1] += 9.8
        self.collision_type = self.collision_checker(tiles)
        if time - self.frame_last_update > self.frame_cooldown:
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
            self.frame_last_update = time
        if self.rect.x > player_x:
            self.facing_right = False
        else:
            self.facing_right = True
    
    def draw(self,display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.facing_right:
            display.blit(self.animation[self.frame], self.rect)
        else:
            flip = self.animation[self.frame].copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect
        

        