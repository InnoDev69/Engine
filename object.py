import pygame
from engineExtends import Render

class GameObject():
    def __init__(self, x, y, width, height, color, texture):
        self.x= x
        self.y= y
        self.width= width
        self.height= height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.texture = None
        if self.color:
            self.surface = pygame.Surface((width, height))
            self.surface.fill(color)
        if texture:
            self.texture = pygame.image.load(texture)
            self.texture = pygame.transform.scale(self.texture, (width, height))

    def draw(self, screen, camera_rect=None):
        dx, dy = (-camera_rect.x, -camera_rect.y) if camera_rect else (0, 0)
        if self.color:
            screen.blit(self.surface, self.rect.move(dx, dy))
        elif self.texture:
            screen.blit(self.texture, self.rect.move(dx, dy))

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

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.is_dragging = True

    def move_with_mouse(self, rel):
        if self.is_dragging:
            self.rect.move_ip(rel)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y