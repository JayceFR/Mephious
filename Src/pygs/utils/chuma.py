import pygame

class Chuma():
    def __init__(self, animation, repeat = True, frame_cooldown = 200) -> None:
        self.animation = animation
        self.frame = 0
        self.frame_upate = 0
        self.repeat = repeat
        self.frame_cooldown = frame_cooldown

    def draw(self, time, display, scroll, loc):
        display.blit(self.animation[self.frame], (loc[0] - scroll[0], loc[1] - scroll[1]))
        if time - self.frame_upate > self.frame_cooldown:
            self.frame_upate = time
            self.frame += 1
            if self.frame >= 4:
                if self.repeat:
                    self.frame = 0
                else:
                    self.frame = 3
    
    def reset_frame(self):
        self.frame = 0
    