import Src.pygs.utils.physics as physics

class Key(physics.PhysicsEntity):
    def __init__(self, loc, width, height):
        super().__init__(loc, width, height)
        self.movement = [0,0]
        self.collision_type = {}
    
    def move(self, tiles):
        self.movement = [0,0]
        self.movement[1] += 9.8
        self.collision_type = self.collision_checker(tiles)
    