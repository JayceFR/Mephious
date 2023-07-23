import pygame, math, random
class Enchanted():
    def __init__(self, loc) -> None:
        self.loc = loc
        self.circles = []
    
    def update(self,loc):
        self.loc = loc
        for x in range(5):
            self.circles.append(Circles(loc[0] + random.randint(0,20), loc[1] + random.randint(-20,20), random.randint(2,4), random.randint(1000, 2000), 0.2, (234,63,247), 2, math.radians(random.randint(0,360))))
    
    def draw(self,time, display, scroll, color = None):
        for pos, circle in sorted(enumerate(self.circles), reverse=True):
            if color == None:
                circle.draw(display, scroll)
            else:
                circle.draw(display, scroll, color)
            circle.move(time)
            if circle.radius < 0:
                self.circles.pop(pos)
    
    def clear(self):
        self.circles.clear()


class Circles():
    def __init__(self,x,y,radius, cooldown, dradius, color = (207,207,207), type = 0, angle=0) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.max_radius = radius + radius * 0.5
        self.min_radius = radius - radius * 0.5
        self.last_update = 0
        self.cooldown = cooldown
        self.angle = angle
        self.dradius = dradius
        self.type = type
        self.color = color
        
    
    def move(self, time):
        if self.type == 0:
            if time - self.last_update > self.cooldown:
                self.radius += self.dradius
                if self.radius > self.max_radius:
                    self.dradius *= -1
                if self.radius < self.min_radius:
                    self.dradius *= -1
                self.last_update = time
        if self.type == 1:
            if time - self.last_update > self.cooldown:
                self.radius -= self.dradius
                self.x += math.cos(self.angle) * 5
                self.y += math.sin(self.angle) * 5
                self.y += 0.7
        if self.type == 2:
            if time - self.last_update > self.cooldown:
                self.radius -= self.dradius
                self.x += math.cos(self.angle) * 5
                self.y -= 1.7
    
    def update_angle(self):
        angle = math.degrees(self.angle)
        angle += random.randint(0,30)
        if angle > 360:
            angle = 0
        self.angle = math.radians(angle)
    

    def draw(self, display, scroll, color = None):
        if color == None:
            pygame.draw.circle(display, self.color, (self.x - scroll[0], self.y - scroll[1]),self.radius)
        else:
            pygame.draw.circle(display, color, (self.x - scroll[0], self.y - scroll[1]),self.radius)