# object.py
import pygame

class GameObject():
    def __init__(self, x, y, width, height, color, texture, velocity):
        self.x= x
        self.y= y
        self.width= width
        self.height= height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.texture = texture
        self.image = pygame.Surface((width, height))  
        self.image.fill(color)  
        self.old_x = self.x
        self.old_y = self.y
        self.velocity = velocity
        self.fvel = velocity 

    def draw(self, screen, camera_rect=None):
        if camera_rect:
            rect_to_draw = self.rect.move(-camera_rect.x, -camera_rect.y)
            screen.blit(self.image, rect_to_draw)
        else:
            screen.blit(self.image, self.rect)

    def update(self):
        self.y += self.velocity
        self.rect.y = self.y
        