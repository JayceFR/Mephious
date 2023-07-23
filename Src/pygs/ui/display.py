import pygame 
from ..shader import shader

class Display():
    def __init__(self, title, screen_w, screen_h, double_up = True, open_gl = False, vertex_loc = "", fragment_loc = ""):
        self.title = title
        self.double_up = double_up
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.open_gl = open_gl
        self.vertex_loc = vertex_loc
        self.fragment_loc = fragment_loc
        self.shader_obj = None
        if double_up:
            if self.open_gl:
                self.screen = pygame.display.set_mode((screen_w, screen_h), pygame.OPENGL | pygame.DOUBLEBUF)
                self.window = pygame.Surface((screen_w, screen_h))
            else:
                self.window = pygame.display.set_mode((screen_w, screen_h))
            self.display = pygame.Surface((screen_w//2, screen_h//2))
        else:
            if self.open_gl:
                self.display = pygame.display.set_mode((screen_w, screen_h), pygame.OPENGL | pygame.DOUBLEBUF)
            else:
                self.display = pygame.display.set_mode((screen_w, screen_h))
        if self.open_gl:
            self.shader_obj = shader.Shader(True, vertex_loc, fragment_loc)
            self.ui_display = pygame.Surface((screen_w//2, screen_h//2), pygame.SRCALPHA)
        pygame.display.set_caption(title)
    
    def redraw(self):
        self.display.fill((0,0,0))
        if self.open_gl:
            self.ui_display.fill((0,0,0,0))

    def clean(self, uniform = {}, variables = {}):
        if self.double_up:
            surf = self.display.copy()
            surf = pygame.transform.scale(surf, (self.screen_w, self.screen_h))
            self.window.blit(surf, (0,0))
        if self.shader_obj:
            uniform['tex'] = self.window
            uniform['ui_tex'] = self.ui_display
            #self.shader_obj.draw({"tex" : self.window, "noise_tex1": noise_img, "ui_tex" : ui_display}, { "itime": int((t.time() - start_time) * 100) })
            self.shader_obj.draw(uniform, variables)
        pygame.display.flip()

    def sillhouette(self, val):
        display_mask = pygame.mask.from_surface(self.display)
        display_sillhoutte = display_mask.to_surface(setcolor=(0,0,0,val), unsetcolor=(0,0,0,0))
        self.blit(display_sillhoutte, (0,0))
    
    def blit(self, img, dest, ui_display = False, special_flag = None):
        if special_flag:
            if not ui_display:
                self.display.blit(img, dest, special_flags=special_flag)
            else:
                self.ui_display.blit(img, dest, special_flags=special_flag )
        else:
            if not ui_display:
                self.display.blit(img, dest)
            else:
                self.ui_display.blit(img, dest)
    
    def draw_polygon(self, color, points):
        pygame.draw.polygon(self.display, color, points)
    
    def draw_circle(self, color, center, radius, ui_display = False):
        if not ui_display:
            pygame.draw.circle(self.display, color, center, radius)
        else:
            pygame.draw.circle(self.ui_display, color, center, radius)
    
        
        

