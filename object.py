import pygame
from engineExtends import Render

class GameObject(Render):
    def __init__(self, x, y, width, height, color, texture):
        self.x= x
        self.y= y
        self.width= width
        self.height= height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.texture = None
        self.animations={}
        self.is_dragging=False
        if self.color:
            self.surface = pygame.Surface((width, height))
            self.surface.fill(color)
        if texture:
            self.texture = pygame.image.load(texture)
            self.texture = pygame.transform.scale(self.texture, (width, height))

    def update(self):
        pass
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Block(GameObject):
    def __init__(self, x, y, block_type, collidable, kill=None, texture=None, color=None):
        super().__init__(x, y, 50, 50, color, texture)
        self.collidable = collidable
        self.block_type = block_type
        self.morido = kill if kill is not None else False

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y