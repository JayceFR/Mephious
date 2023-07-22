import pygame
class Misc():
    def __init__(self) -> None:
        self
    
    def load_img(self, loc, color_key,  rotation = 0, scale = 0, scale_coords = None):
        curr_img = pygame.image.load(loc).convert_alpha()
        if rotation > 0:
            curr_img = pygame.transform.rotate(curr_img, rotation)
        if scale > 0 or scale_coords:
            if not scale_coords:
                curr_img = pygame.transform.scale(curr_img, (curr_img.get_width()*scale, curr_img.get_height()*scale))
            else:
                curr_img = pygame.transform.scale(curr_img, scale_coords)
        if not color_key == None:
            curr_img.set_colorkey(color_key)
        return curr_img
    
    def get_image(self, sheet, frame, width, height, scale, colorkey, scale_coordinates = []):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        if scale_coordinates == []:
            image = pygame.transform.scale(image, (width * scale, height * scale))
        else:
            image = pygame.transform.scale(image, scale_coordinates )
        image.set_colorkey(colorkey)
        return image
    
    def load_animation(self, loc, number_of_frames, scale, colorkey, scale_coords = []):
        sheet = self.load_img(loc, color_key=None)
        animation = []
        print(sheet.get_width()//number_of_frames)
        for x in range(number_of_frames):
            animation.append(self.get_image(sheet, x, sheet.get_width()//number_of_frames, sheet.get_height(), scale, colorkey, scale_coords ))
        return animation
    
    def rotate_img(self, surf, angle):
        image = surf.copy()
        image = pygame.transform.rotate(image, angle)
        return image
