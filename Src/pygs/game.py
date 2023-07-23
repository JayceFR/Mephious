#Speech for fruits
#Corrupting of banana
#Map 
#Music
#Cover page
from .ui import display, grass, fireflies, bg_particles, rot
from .entities import player, key as keys, fruits as fruit
from .map import map
from .utils import typewriter, chuma
import pygame, random, math, time as t
class Game():
    def __init__(self, window_size = [0,0], double_buf = True, is_shader = False, vertex_loc = "", fragment_loc = ""):
        self.run = True
        self.window_size = window_size
        self.double_buf = double_buf
        self.shader_stuf = {}
        pygame.init()
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
        self.strawberry_loc = self.entity_loc['s'][0]
        self.orange_loc = self.entity_loc['r'][0]
        self.pineapple_loc = self.entity_loc['a'][0]
        self.pineapple = fruit.Fruits(self.pineapple_loc, game_items['map'].get('entities')['a'][0])
        self.pineapple_chuma = chuma.Chuma(game_items['map'].get('entities')['a'][1])
        self.orange = fruit.Fruits(self.orange_loc, game_items['map'].get('entities')['r'][0])
        self.orange_chuma = chuma.Chuma(game_items['map'].get('entities')['r'][1])
        self.strawberry = fruit.Fruits(self.strawberry_loc, game_items['map'].get('entities')['s'][0])
        self.strawberry_chuma = chuma.Chuma(game_items['map'].get('entities')['s'][1])
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
        self.grass_cooldown = 70
    
    def blit_grass(self, grasses, display, scroll, player):
        for grass in grasses:
            if grass.get_rect().colliderect(player.get_rect()):
                grass.colliding()
            grass.draw(display, scroll)
    
    def draw_text(text, font, text_col, x, y, display):
        img = font.render(text, True, text_col)
        display.blit(img, (x, y))
        
    def game_loop(self):
        true_scroll = [0,0]
        start_time = t.time()
        shader_time = 0
        show_map = False
        #silhouette
        val = 0
        #toxic gas
        gas_val = 0.1549
        key = keys.Key([0,0], 16, 16)
        key.move(self.tile_rects)
        interact_sound = pygame.mixer.Sound("./Assets/Music/interact.wav")
        interact_sound.set_volume(0.2)
        font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 18)
        typer = typewriter.TypeWriter(font, (255,255,255), 100, 180, 300, 9, interact_sound)
        scissor_map = pygame.image.load("./Assets/Entities/scissor_map.png").convert_alpha()
        scissor_map.set_colorkey((0,0,0))
        candle_map = pygame.image.load("./Assets/Entities/candle_map.png").convert_alpha()
        candle_map.set_colorkey((0,0,0))
        strawberry_text = [{"text" : ["Hey son", "Mr.Orange wanted your red paint", "That's funny I thought he never liked red", "I am running out of time, please...", "Hmmm.. what would I get in return", "But.... I am corrupted and I would die soon", "I don't care about you", "Ok, what do you want", "Bring me a pair of scissors from Mr.Pineapple", "Let me guess, for your hair?", "Nah, just to get something in return"],
                            "can_show" : False,
                            "before_me": "pineapple",
                            "who_is_next" : "orange", 
                            "whoami" : "strawberry",
                            "default" : False }, 
                            {"text" : ["Mr.Pineapple was looking for you"],
                             "default" : True, 
                             "can_show" : False,
                             "whoami" : "strawberry"
                            }]
        orange_text = [{"text" : ["If this is not a dream, the Corrupted Mephoius banana in flesh", "Wow, that was spooky", "What brings you here?", "I need to deliver a pair of scissors to Ms.Strawberry", "Oh! There is a problem in that", "What?", "My scissors were stolen and buried by Mr.Pineapple", "I hate that pineapple", "You can find the location of the scissors in this map", "Thank you"],
                            "can_show" : False,
                            "before_me" : "strawberry",
                            "who_is_next" : "scissor_map", 
                            "whoami" : "orange",
                            "default" : False },
                        {"text" : ["How long can you live before the corruption takes you"],
                         "default" : True,
                         "can_show" : False,
                         "whoami" : "orange"}]
        pineapple_text = [{"text" : ["Hey chap, any plans for tomorrow?", "Hmmm...", "Except corrupting and rotting to death... lol", "Can I please borrow your vitamin B9", "Hmmm.. what would I get in return", "But I am going to rot soon", "I don't care about you", "Ok, what do you want", "Go get the red paint from Ms.Strawberry", "Why?", "For my car, GET IT"],
                            "can_show" : True,
                            "default" : False,
                            "whoami" : "pineapple",
                            "who_is_next" : "strawberry" }, 
                            {"text" : ["Where is my paint?"],
                             "can_show" : False,
                             "default" : True, 
                             "whoami" : "pineapple"}]
        fruits = {"strawberry" : [self.strawberry, strawberry_text, self.strawberry_chuma, [0,125]], "orange" : [self.orange, orange_text, self.orange_chuma, [0,150]], "pineapple" : [self.pineapple, pineapple_text, self.pineapple_chuma, [-20, 125]]}
        final_destination = [[scissor_map, (1942, 1152), False], [candle_map, (2030, 1412), False]]
        inventory = [] # [img, loc]
        write_text = False
        click = False
        corruption_last_update = 0
        corruption_cooldown = 60
        corruption_level = 0
        corrupt_binary = 1
        change_corruption = False
        change_corruption_last_update = 0
        corruption_particles = rot.Enchanted([1000,400])
        shader_val = 0
        print(len(self.grasses))
        while self.run:
            
            self.clock.tick(60)
            #print(round(self.clock.get_fps()))
            shader_time += 0.025
            time = pygame.time.get_ticks()
            second_time = round(t.time() - start_time)
            if second_time - corruption_last_update > corruption_cooldown:
                corruption_last_update = second_time
                corruption_level += 1
                change_corruption = True
                shader_val += 0.1
                print(shader_val)
                change_corruption_last_update = time
                self.player.change_corruption_level(corruption_level)
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
            self.player.move(self.tile_rects, time, write_text)
            self.player.draw(time, self.display, scroll)
            if change_corruption:
                if time - change_corruption_last_update < 10000:
                    val = 50
                    corrupt_binary = 0
                    corruption_particles.update([self.player.get_rect().x, self.player.get_rect().y + 15])
                    corruption_particles.draw(time, self.display.display, scroll, (55,55,55))
                else:
                    corruption_particles.clear()
                    val = 0
                    change_corruption = False
                    corrupt_binary = 1
            #Moving and drawing fruits
            for key in fruits.keys():
                fruits[key][0].move(time, self.tile_rects, self.player.get_rect().x)
                fruits[key][0].draw(self.display, scroll)
                if pygame.rect.Rect(fruits[key][0].get_rect().x -20, fruits[key][0].get_rect().y, fruits[key][0].get_rect().width * 2, fruits[key][0].get_rect().height ).colliderect(self.player.get_rect()):
                    if click:
                        if write_text == False:
                            write_text = True
                            #typer.write(fruits[key][1])
                            correct_dict = {}
                            for pos, dict in sorted(enumerate(fruits[key][1]), reverse=True):
                                if dict['can_show']:
                                    correct_dict = fruits[key][1].pop(pos)
                            if correct_dict == {}:
                                for dict in fruits[key][1]:
                                    if dict['default']:
                                        correct_dict = dict
                            typer.write(correct_dict['text'])
            if write_text:
                write_text = not typer.update(time, self.display.ui_display, [350, 220], fruits[correct_dict['whoami']][2])
                fruits[correct_dict['whoami']][2].draw(time, self.display.ui_display, [0,0], fruits[correct_dict['whoami']][3])
                if not write_text and not correct_dict['default']:
                    next_key = correct_dict['who_is_next']
                    if fruits.get(next_key) != None:
                        for dict in fruits.get(next_key)[1]:
                            if not dict['default']:
                                if dict['before_me'] == correct_dict['whoami']:
                                    dict['can_show'] = True
                    elif next_key == "scissor_map":
                        final_destination[0][2] = True
                        inventory = [final_destination[0][0], [-25,20]]
                    if dict['whoami'] == "strawberry":
                        fruits['strawberry'][1][1]['text'] = ["Where are my scissors?" ]
            

            if show_map:
                if inventory != []:
                    self.display.ui_display.blit(inventory[0], inventory[1])
            
            #Sillhouette
            self.display.sillhouette(val)
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
            
            for destination in final_destination:
                if destination[2] == True:
                    if self.player.get_rect().collidepoint(destination[1]):
                        print("I am here")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if not show_map:
                            show_map = True
                        else:
                            show_map = False
            self.display.clean({"noise_tex1": self.shader_stuf['noise_img']}, { "itime": int((t.time() - start_time) * 100), "time" : shader_time, "corrupted" : corrupt_binary, "shader_val" : shader_val})
