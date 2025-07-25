import pygame

class Particle:
    def __init__(self, x, y, color, speed, lifetime, depth, radius, gravity_factor=0, collision_enabled=True):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.lifetime = lifetime
        self.timer = 0
        self.depth = depth
        self.radius = radius
        self.gravity_factor = gravity_factor
        self.collision_enabled = collision_enabled

    def draw(self, screen):
        adjusted_x = int(self.x - self.radius * self.depth)
        adjusted_y = int(self.y - self.radius * self.depth)
        adjusted_radius = int(self.radius * (1 + self.depth / 10))  # Ajusta el radio que se basa en la profundidad

        z_position = self.y + self.depth

        pygame.draw.circle(screen, self.color, (adjusted_x, adjusted_y), adjusted_radius)

        # Línea que representaria el eje Z
        #pygame.draw.line(screen, (255, 255, 255), (adjusted_x, adjusted_y), (adjusted_x, z_position), 1)
    def update(self):
        if self.timer < self.lifetime:
            self.speed = (self.speed[0], self.speed[1] + self.gravity_factor)
            self.x += self.speed[0]
            self.y += self.speed[1]
            self.timer += 1

