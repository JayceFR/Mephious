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
        print("tile",self.rect.x, self.rect.y)
        display.blit(self.img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    
    def get_rect(self):
        return self.rect

class Map():
    def __init__(self, map_loc, width_of_tiles, location_of_tiles, is_there_collide_tiles = True, is_there_non_collide_tiles = False, entities = {}) -> None:
        self.entities = entities
        self.list_of_available_signs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "$", "%", "^", "&", "*", "-", "+", ":", ";", "<", ">", "/", "~", "|"]
        self.chunks = {}
        self.width_of_tiles = width_of_tiles
        self.collide_length = 0
        non_collide_length = 0
        if is_there_collide_tiles:
            tile_names = os.listdir(location_of_tiles + "/collide")
            self.collide_length = len(tile_names)
            tile_names.sort()
            self.tile_imgs = []
            for x in range(len(tile_names)):
                curr_tile = pygame.image.load(location_of_tiles + "/collide/" + "tile" + str(x+1)+ ".png").convert_alpha()
                curr_tile = pygame.transform.scale(curr_tile, (width_of_tiles, width_of_tiles))
                curr_tile.set_colorkey((0,0,0))
                self.tile_imgs.append(curr_tile)
        if is_there_non_collide_tiles:
            tile_names = os.listdir(location_of_tiles + "/non_collide")
            self.non_collide_length = self.collide_length +  len(tile_names)
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
        print(len(map[0]))
        print("No.of.chunks", (len(map) * len(map[0]) - (8 * 8)))
        no_of_chunks = (len(map) * len(map[0])) - (8 * 8)
        start_x = 0
        end_x = 8
        target_start_x = 0
        target_end_x = 8
        for x in range(6): #48//8
            print("target_start_x", target_start_x, "target_end_x", target_end_x)
            for y in range(23): #184//8
                chunk_one = []
                for z in range(target_start_x, target_end_x):
                    chunk_one.append(map[z][start_x:end_x])
                self.chunks[str(target_start_x) + ":" + str(start_x)] = chunk_one
                start_x = end_x
                end_x += 8
                #print(chunk_one)
            target_start_x = target_end_x
            target_end_x += 8
            start_x = 0
            end_x = 8
        print(self.chunks)
    
    def load_chunk(self, player_loc):
        find_key = [round((player_loc[0]/32)/8), round((player_loc[1]/32)/8)]
        print(find_key)
        curr_key = str((find_key[1]) * 8) + ":" + str(find_key[0] * 8)
        if curr_key in self.chunks.keys():
            map = self.chunks[curr_key]
            return map

    def load_game_enitites(self, player_loc):
        print("actual_player_loc = ", player_loc)
        map = self.load_chunk(player_loc)
        self.tile_rects = []
        y = 0
        for row in map:
            x = 0
            for element in row:
                pos = 0
                while pos < len(self.list_of_available_signs) and self.list_of_available_signs[pos] != element:
                    pos += 1
                if element == "&":
                    self.tile_rects.append(Tiles(x*self.width_of_tiles, y*self.width_of_tiles, self.width_of_tiles, self.width_of_tiles, self.tile_imgs[pos], ramp=True))
                elif element == "*":
                    self.tile_rects.append(Tiles(x*self.width_of_tiles, y*self.width_of_tiles, self.width_of_tiles, self.width_of_tiles, self.tile_imgs[pos], ramp=True, ramp_type=2))
                elif pos < len(self.list_of_available_signs) and pos < self.collide_length:
                    self.tile_rects.append(Tiles(x*self.width_of_tiles, y*self.width_of_tiles, self.width_of_tiles, self.width_of_tiles, self.tile_imgs[pos]))
                elif pos < len(self.list_of_available_signs) and pos < self.non_collide_length:
                    self.tile_rects.append(Tiles(x*self.width_of_tiles, y*self.width_of_tiles, self.width_of_tiles, self.width_of_tiles, self.tile_imgs[pos], False))
                elif element in self.entities:
                    self.entities[element].append([x*self.width_of_tiles, y*self.width_of_tiles])
                x += 1
            y += 1
    
    def draw(self, display, scroll):
        for tile in self.tile_rects:
            tile.draw(display, scroll)
    
    def get_rect(self):
        return self.tile_rects, self.entities