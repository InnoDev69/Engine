import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

    def load_sound(self, sound_name, sound_file):
        sound = pygame.mixer.Sound(sound_file)
        self.sounds[sound_name] = sound

    def play(self, sound_name):
        if sound_name in this.sounds:
            this.sounds[sound_name].play()

    def stop(self, sound_name):
        if sound_name in this.sounds:
            this.sounds[sound_name].stop()
