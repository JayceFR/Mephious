from .ui import display, grass, fireflies, bg_particles
from .entities import player, key as keys
from .map import map
import pygame, random, math, time as t
class Game():
    def __init__(self, window_size = [0,0], double_buf = True, is_shader = False, vertex_loc = "", fragment_loc = ""):
        self.run = True
        self.window_size = window_size
        self.double_buf = double_buf
        self.shader_stuf = {}
        self.display = display.Display("Mephious", self.window_size[0], self.window_size[1], self.double_buf)
        if is_shader:
            self.display = display.Display("Mephious", self.window_size[0], self.window_size[1], self.double_buf, True, vertex_loc, fragment_loc )
        else:
            self.display = display.Display("Mephious", self.window_size[0], self.window_size[1], self.double_buf)
        
    def load_game_items(self, game_items = {'player' : {}, 'map' : {}, 'world' : {}}):
        self.shader_stuf = game_items['world']['shader']
        entities = {}
        if game_items['map'].get('entities'):
            for entity in game_items['map']['entities'].keys():
                entities[entity] = []
        print(entities)
        self.e_entities = game_items['map'].get('entities')
        self.map = map.Map(game_items['map']['map_loc'], game_items['map']['width_of_tiles'], game_items['map']['location_of_tiles'], game_items['map']['is_there_collide_tiles'], game_items['map']['is_there_non_collide_tiles'], entities )
        self.tile_rects, self.entity_loc = self.map.get_rect()
        self.player = player.Player(game_items['player'])
        self.game_items = game_items
        self.clock = pygame.time.Clock()
        #Grass
        self.grasses = []
        for loc in self.entity_loc['g']:
            x_pos = loc[0]
            while x_pos < loc[0] + 32:
                x_pos += 2.5
                height = random.randint(3,15)
                self.grasses.append(grass.grass([x_pos, loc[1]+(14*2) - (height - 9) ], 2, height))
        if game_items['map'].get("ignore_entities"):
            for key in game_items['map']['ignore_entities']:
                self.e_entities.pop(key)
        self.firefly = None
        if game_items['world'].get("fireflies"):
            self.firefly = fireflies.Fireflies(0, 100, 6000, 1200)
        self.bg_particle_effect = None
        if game_items['world'].get("leaves")[0]:
            self.bg_particle_effect = bg_particles.Master(game_items['world']['leaves'][1])
        self.entity_loc.pop("g")
        self.grass_last_update = 0
        self.grass_cooldown = 50
    
    def blit_grass(self, grasses, display, scroll, player):
        for grass in grasses:
            if grass.get_rect().colliderect(player.get_rect()):
                grass.colliding()
            grass.draw(display, scroll)
    
    def game_loop(self):
        true_scroll = [0,0]
        start_time = t.time()
        #silhouette
        val = 0
        #toxic gas
        gas_val = 0.1549
        key = keys.Key([0,0], 16, 16)
        key.move(self.tile_rects)
        while self.run:
            self.clock.tick(60)
            time = pygame.time.get_ticks()
            self.display.redraw()
            #Normal code
            true_scroll[0] += (self.player.get_rect().x - true_scroll[0] - 202) 
            true_scroll[1] += (self.player.get_rect().y - true_scroll[1] - 132) 
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])
            self.map.draw(self.display, scroll)
            #Blitting entities
            for key in self.e_entities.keys():
                for loc in self.entity_loc[key]:
                    self.display.blit(self.e_entities[key][0], (loc[0] - scroll[0] - self.e_entities[key][1][0], loc[1] - scroll[1] - self.e_entities[key][1][1]))
            self.player.move(self.tile_rects, time)
            self.player.draw(time, self.display, scroll)
            '''
            #Sillhouette
            self.display.sillhouette(val)
            val += 1
            if val > 255:
                val = 0'''
            #grass movement
            if time - self.grass_last_update > self.grass_cooldown:
                for grass in self.grasses:
                    grass.move()
                self.grass_last_update = time
            self.blit_grass(self.grasses, self.display, scroll, self.player)
            if self.bg_particle_effect:
                self.bg_particle_effect.recursive_call(time, self.display, scroll, 1)
            if self.firefly:
                self.firefly.recursive_call(time, self.display, scroll)
            self.run = self.display.clean({"noise_tex1": self.shader_stuf['noise_img']}, { "itime": int((t.time() - start_time) * 100) })
