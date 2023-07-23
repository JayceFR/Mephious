import pygame
import Src.pygs.game as game
import Src.pygs.utils.misc as misc

#loading images
help = misc.Misc()
e = game.Game([800,500], True, is_shader= True, vertex_loc= "./Src/shader/vertex.vert", fragment_loc= "./Src/shader/fragment.frag" )
#player
idle_animation = help.load_animation("./Assets/Sprites/banana_idle.png", 4, 1, (255,255,255))
print(idle_animation)
run_animation = help.load_animation("./Assets/Sprites/banana_run.png", 4, 1, (255,255,255))
jump_spark_animation = help.load_animation("./Assets/Entities/jump_spark.png", 4, 1, (0,0,0))
jump_img = help.load_img("./Assets/Sprites/banana_jump.png", (255,255,255), 0,1)
fall_img = help.load_img("./Assets/Sprites/banana_jump.png", (255,255,255), -25, 1)
#entities
orange_tree = help.load_img("./Assets/Entities/tree1.png", (255,255,255), scale=1.5)
pink_tree = help.load_img("./Assets/Entities/tree2.png", (255,255,255), scale=1.5)
fence = help.load_img("./Assets/Entities/fence.png", (255,255,255), scale_coords=[32,19])
leaf_img = pygame.image.load("./Assets/Entities/leaf.png").convert_alpha()
leaf_img.set_colorkey((0,0,0))
leaf_img2 = pygame.image.load("./Assets/Entities/leaf2.png").convert_alpha()
leaf_img2.set_colorkey((0,0,0))
orange_idle_ani = help.load_animation("./Assets/Sprites/orange_idle.png", 4, 1, (118, 66, 138))
pineapple_idle_ani = help.load_animation("./Assets/Sprites/pineapple_idle.png", 4, 1, (118, 66, 138))
strawberry_idle_ani = help.load_animation("./Assets/Sprites/strawberry_idle.png", 4, 1, (118, 66, 138 ))
orange_talk_ani = help.load_animation("./Assets/Sprites/orange_talk.png", 4, 2, (118, 66, 138))
pineapple_talk_ani = help.load_animation("./Assets/Sprites/pineapple_talk.png", 4, 2, (118, 66, 138))
strawberry_talk_ani = help.load_animation("./Assets/Sprites/strawberry_talk.png", 4, 2, (118, 66, 138))
idle_animations = [idle_animation]
run_animations = [run_animation]
jump_frames = [jump_img]
fall_frames = [fall_img]
for x in range(4):
    idle_animations.append(help.load_animation("./Assets/Sprites/banana_idle_stage_" + str(x+1) + ".png", 4, 1, (255,255,255)))
    run_animations.append(help.load_animation("./Assets/Sprites/banana_run_stage_" + str(x+1) + ".png", 4, 1, (255,255,255)))
    jump_frames.append(help.load_img("./Assets/Sprites/banana_jump_stage_" + str(x+1) + ".png", (255,255,255), 0,1))
    fall_frames.append(help.load_img("./Assets/Sprites/banana_jump_stage_" + str(x+1) + ".png", (255,255,255), 0,1))

noise_img = pygame.image.load("./Src/shader/pnoise.png").convert_alpha()

pass_e_game = {
    'player' : {
        'x' : 1000, 
        'y' : 400, 
        'width' : idle_animation[0].get_width(), 
        'height': idle_animation[0].get_height(), 
        'idle_animation' : idle_animations, 
        'run_animation' : run_animations, 
        'jump_img' : jump_frames, 
        'fall_img': fall_frames,
        'jump_spark_ani' : jump_spark_animation
        },
    'map' : {
        'map_loc' : "./Assets/Maps/level1.txt", 
        'width_of_tiles': 32, 
        'location_of_tiles' : "./Assets/Tiles", 
        'is_there_collide_tiles' : True, 
        'is_there_non_collide_tiles': True,
        'entities' : {
            "g" : [],
            "s" : [strawberry_idle_ani, strawberry_talk_ani], # strawberry
            "r" : [orange_idle_ani, orange_talk_ani], # orange
            "a" : [pineapple_idle_ani, pineapple_talk_ani], # pineapple
            "o" : [orange_tree, [69,110]],
            "p" : [pink_tree, [69,105]],
            "f" : [fence, [0, -12]],
            },
        'ignore_entities' : ["g", "s", "r", "a"]
        },
    'world' : {
        'leaves' : [True, [leaf_img, leaf_img2]],
        'fireflies' : True,
        'shader': {
            'is_shader' : True,
            'noise_img' : noise_img,
            'vertex_loc' : "./Src/shader/vertex.vert",
            'fragment_loc' : "./Src/shader/fragment.frag"
        }
        },
    }

e.load_game_items(pass_e_game)
e.game_loop()