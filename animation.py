import pygame

class Animation:
    def __init__(self, frames):
        self.frames = frames
        self.frame_index = 0
        self.frame_rate = 10
        self.frame_counter = 0

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0

    def current_frame(self):
        return self.frames[self.frame_index]
