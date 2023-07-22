import pygame
import os 

class Tiles():
    def __init__(self, x, y, width, height, img, touchable = True, ramp = False, ramp_type = 1) -> None:
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.img = img
        self.touchable = touchable
        self.ramp = ramp
        self.ramp_type = ramp_type
    
    def draw(self, display, scroll):
        display.blit(self.img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    
    def get_rect(self):
        return self.rect

class Map():
    def __init__(self, map_loc, width_of_tiles, location_of_tiles, is_there_collide_tiles = True, is_there_non_collide_tiles = False, entities = {}) -> None:
        self.entities = entities
        self.list_of_available_signs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "$", "%", "^", "&", "*", "-", "+", ":", ";", "<", ">", "/", "~", "|"]
        collide_length = 0
        non_collide_length = 0
        if is_there_collide_tiles:
            tile_names = os.listdir(location_of_tiles + "/collide")
            collide_length = len(tile_names)
            tile_names.sort()
            self.tile_imgs = []
            for x in range(len(tile_names)):
                curr_tile = pygame.image.load(location_of_tiles + "/collide/" + "tile" + str(x+1)+ ".png").convert_alpha()
                curr_tile = pygame.transform.scale(curr_tile, (width_of_tiles, width_of_tiles))
                curr_tile.set_colorkey((0,0,0))
                self.tile_imgs.append(curr_tile)
        if is_there_non_collide_tiles:
            tile_names = os.listdir(location_of_tiles + "/non_collide")
            non_collide_length = collide_length +  len(tile_names)
            tile_names.sort()
            for tile_name in tile_names:
                curr_tile = pygame.image.load(location_of_tiles + "/non_collide/" + tile_name).convert_alpha()
                curr_tile = pygame.transform.scale(curr_tile, (width_of_tiles, width_of_tiles))
                curr_tile.set_colorkey((0,0,0))
                self.tile_imgs.append(curr_tile)
        self.tile_rects = []
        map = []
        f = open(map_loc, "r")
        data = f.read()
        f.close()
        data = data.split("\n")
        for row in data:
            map.append(list(row))
        y = 0
        for row in map:
            x = 0
            for element in row:
                pos = 0
                while pos < len(self.list_of_available_signs) and self.list_of_available_signs[pos] != element:
                    pos += 1
                if element == "&":
                    self.tile_rects.append(Tiles(x*width_of_tiles, y*width_of_tiles, width_of_tiles, width_of_tiles, self.tile_imgs[pos], ramp=True))
                elif element == "*":
                    self.tile_rects.append(Tiles(x*width_of_tiles, y*width_of_tiles, width_of_tiles, width_of_tiles, self.tile_imgs[pos], ramp=True, ramp_type=2))
                elif pos < len(self.list_of_available_signs) and pos < collide_length:
                    self.tile_rects.append(Tiles(x*width_of_tiles, y*width_of_tiles, width_of_tiles, width_of_tiles, self.tile_imgs[pos]))
                elif pos < len(self.list_of_available_signs) and pos < non_collide_length:
                    self.tile_rects.append(Tiles(x*width_of_tiles, y*width_of_tiles, width_of_tiles, width_of_tiles, self.tile_imgs[pos], False))
                elif element in self.entities:
                    self.entities[element].append([x*width_of_tiles, y*width_of_tiles])
                x += 1
            y += 1
    
    def draw(self, display, scroll):
        for tile in self.tile_rects:
            tile.draw(display, scroll)
    
    def get_rect(self):
        return self.tile_rects, self.entities