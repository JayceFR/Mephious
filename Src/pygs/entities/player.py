import pygame
from pygame.locals import *
import Src.pygs.utils.misc as misc
import Src.pygs.utils.chuma as chuma
class Player():
    #items keys :  x, y, width, height, idle_animation, run_animation, jump_img, fall_img) -> None:
    def __init__(self, items, replace_x = None, replace_y = None):
        if replace_x or replace_y:
            self.rect = pygame.rect.Rect(replace_x, replace_y, items['width'], items['height'])    
        else:
            self.rect = pygame.rect.Rect(items['x'], items['y'], items['width'], items['height'])
        self.movement = [0,0]
        self.display_x = 0
        self.display_y = 0
        self.moving_left = False
        self.moving_right = False
        self.collision_type = {}
        self.speed = 4
        self.display_x = 0
        self.display_y = 0
        self.idle_animation = items['idle_animation']
        self.run_animation = items['run_animation']
        self.frame = 0
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.facing_right = True
        self.jump = False
        self.jump_img = items['jump_img']
        self.fall_img = items['fall_img']
        self.jump_last_update = 0
        self.radius = items['width'] * 2
        self.jump_cooldown = 200
        self.jump_up_spped = 9
        self.air_timer = 0
        self.falling = False
        self.jump_count = 2
        self.rotate_jump = False
        self.angle_rot = 0
        self.help = misc.Misc()
        self.corrupt_stage = 0
        #Jump sparks
        self.jump_spark_ani = chuma.Chuma(items['jump_spark_ani'])
        self.jump_loc = []

    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if tile.touchable:
                if self.rect.colliderect(tile.get_rect()):
                    hitlist.append(tile)
        return hitlist
    
    def collision_checker(self, tiles):
        collision_types = {"top": [False, []], "bottom": [False, []], "right": [False, []], "left": [False, []]}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if not tile.ramp:
                if self.movement[0] > 0:
                    self.rect.right = tile.get_rect().left
                    collision_types["right"][0] = True
                    collision_types["right"][1].append(tile)
                elif self.movement[0] < 0:
                    self.rect.left = tile.get_rect().right
                    collision_types["left"][0] = True
                    collision_types["left"][1].append(tile)
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if not tile.ramp:
                if self.movement[1] > 0:
                    self.rect.bottom = tile.get_rect().top
                    collision_types["bottom"][0] = True
                    collision_types["bottom"][1].append(tile)
                if self.movement[1] < 0:
                    self.rect.top = tile.get_rect().bottom
                    collision_types["top"][0] = True
                    collision_types['top'][1].append(tile)
        
        for tile in hit_list:
            if tile.ramp == True:
                rel_x = self.rect.x - tile.get_rect().x
                if tile.ramp_type == 1:
                    pos_height = rel_x + self.rect.width
                elif tile.ramp_type == 2:
                    pos_height = 32 - rel_x
                pos_height = min(pos_height, 32)
                pos_height = max(pos_height, 0)
                target_y = tile.get_rect().y + 32 - pos_height
                if self.rect.bottom > target_y:
                    self.rect.bottom = target_y
                    collision_types["bottom"][0] = True
                    self.movement[1] = self.rect.y
        return collision_types
    
    def move(self, tiles, time, write_text):
        self.movement = [0, 0]

        if self.moving_right:
            self.facing_right = True
            self.movement[0] += self.speed
            self.moving_right = False
        if self.moving_left:
            self.facing_right = False
            self.movement[0] -= self.speed
            self.moving_left = False
        if self.jump:
            if self.air_timer < 40:
                self.air_timer += 1
                self.movement[1] -= self.jump_up_spped
                self.jump_up_spped -= 0.5
            else:
                self.air_timer = 0
                self.jump = False
                self.jump_up_spped = 9

        if time - self.frame_last_update > self.frame_cooldown:
            self.frame_last_update = time
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0

        if not self.jump:
            self.movement[1] += 8

        if self.rotate_jump:
            self.angle_rot -= 15
            if self.angle_rot < -360:
                self.angle_rot = 0
        

        self.collision_type = self.collision_checker(tiles)

        if not self.collision_type['bottom'][0]:
            self.falling = True
        else:
            self.jump_count = 2
            self.rotate_jump = False
            self.angle_rot = 0
            self.falling = False
        if not write_text:
            key = pygame.key.get_pressed()
            if  key[pygame.K_a] or key[pygame.K_LEFT]:
                self.moving_left = True
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                self.moving_right = True
            if key[pygame.K_SPACE] or key[pygame.K_w]:
                if self.jump_count > 0:
                    if time - self.jump_last_update > self.jump_cooldown:
                        #self.music.play()
                        self.jump = True
                        self.air_timer = 0
                        self.jump_loc = [self.rect.x, self.rect.y + 32]
                        self.jump_spark_ani.reset_frame()
                        self.jump_up_spped = 9
                        if self.jump_count == 1:
                            self.rotate_jump = True
                        self.jump_count -= 1
                        self.jump_last_update = time
    
    def change_corruption_level(self, stage):
        self.corrupt_stage = max(0, stage)
    
    def draw(self, time, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.air_timer >= 1 and self.air_timer > 20:
            if self.facing_right:
                display.blit(self.fall_img[self.corrupt_stage], self.rect)
            else:
                flip = self.fall_img[self.corrupt_stage].copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
        elif not self.jump and  self.falling:
            if self.facing_right:
                display.blit(self.fall_img[self.corrupt_stage], self.rect)
            else:
                flip = self.fall_img[self.corrupt_stage].copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
        elif self.jump:
            self.jump_spark_ani.draw(time, display, scroll, self.jump_loc)
            if not self.rotate_jump:
                if self.facing_right:
                    display.blit(self.jump_img[self.corrupt_stage], self.rect)
                else:
                    flip = self.jump_img[self.corrupt_stage].copy()
                    flip = pygame.transform.flip(flip, True, False)
                    display.blit(flip, self.rect)
            else:
                roto_jump = self.help.rotate_img(self.jump_img[self.corrupt_stage], self.angle_rot)
                if self.facing_right:
                    display.blit(roto_jump, self.rect)
                else:
                    flip = roto_jump.copy()
                    flip = pygame.transform.flip(flip, True, False)
                    display.blit(flip, self.rect)
        elif self.moving_right:
            display.blit(self.run_animation[self.corrupt_stage][self.frame], self.rect)
        elif self.moving_left:
            flip = self.run_animation[self.corrupt_stage][self.frame].copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        else:
            if self.facing_right:
                display.blit(self.idle_animation[self.corrupt_stage][self.frame], self.rect)
            else:
                flip = self.idle_animation[self.corrupt_stage][self.frame].copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
        
        display.blit(self.circle_surf(), (self.rect.x - 30, self.rect.y - 20), special_flag=BLEND_RGBA_ADD)

        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect

    def circle_surf(self):
        surf = pygame.Surface((self.radius * 4, self.radius * 4))
        pygame.draw.circle(surf, (20, 20,20), (self.radius, self.radius), self.radius)
        surf.set_colorkey((0, 0, 0))
        return surf
