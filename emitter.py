# emitter.py
import random
import math
from particle import Particle

class ParticleEmitter:
    def __init__(self, x, y, zone_x, zone_y, zone_width, zone_height, spawn_frequency=0.1):
        self.x = x
        self.y = y
        self.zone_x = zone_x
        self.zone_y = zone_y
        self.zone_width = zone_width
        self.zone_height = zone_height
        self.particles = []
        self.spawn_frequency = spawn_frequency
        self.spawn_timer = 0

    def generate_particle(self, radius):
        particle_x = random.uniform(self.zone_x, self.zone_x + self.zone_width)
        particle_y = random.uniform(self.zone_y, self.zone_y + self.zone_height)
        angle = random.uniform(0, 2 * math.pi)  # Ángulo en radianes
        speed_magnitude = random.uniform(1, 5)  # Magnitud de la velocidad
        speed = (speed_magnitude * math.cos(angle), speed_magnitude * math.sin(angle))
        lifetime = random.randint(30, 360)  # Tiempo de vida en fotogramas
        depth = random.randint(-5, 5)  # Profundidad en el eje z
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        gravity_factor = random.uniform(-0.1, 0.1)  # Ajusta la gravedad aleatoriamente
        new_particle = Particle(particle_x, particle_y, color, speed, lifetime, depth, radius, gravity_factor,collision_enabled=True)
        self.particles.append(new_particle)

    def update_particles(self):
        for particle in self.particles:
            particle.update()

        self.particles = [
            particle for particle in self.particles
            if particle.timer < particle.lifetime
        ]

        self.spawn_timer += 1

        if self.spawn_timer >= int(1 / self.spawn_frequency):
            self.generate_particle(5)  
            self.spawn_timer = 0
    def handle_collisions(self, game):
        for particle in self.particles:
            particle.handle_collisions(game)