import pygame

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def particle_object_collision(particle, game_object):
    if particle.collision_enabled and game_object.collision_enabled:
        return check_collision(particle.rect, game_object.rect)
    return False

def particle_particle_collision(particle1, particle2):
    if particle1.collision_enabled and particle2.collision_enabled:
        return check_collision(particle1.rect, particle2.rect)
    return False
