import random

import Fish
import pygame
import Setting
class Shark(Fish.Fish):
    def __init__(self, id, speed, color, rect, vector=None, refresh= 0):
        super().__init__(id, speed, color, rect, vector, refresh)
        self.follow_fish = False


    def update_move(self, fishs, dt):
        # movement by view
        self.close_fish.clear()
        angle = self.vector.angle_to((0, 0))
        for fish in fishs:
            if fish.id == self.id:
                continue

            dist = pygame.Vector2(self.rect.center).distance_to(fish.rect.center)

            if dist < Setting.view_fish:
                new_vec = pygame.Vector2((fish.rect.x - self.rect.x), (fish.rect.y - self.rect.y))
                if new_vec.length_squared() > 0:
                    new_vec.normalize()
                angle_dif = angle - new_vec.angle_to((0, 0))
                if -35 < (angle_dif) < 35:
                    self.close_fish.append((angle_dif, fish))

        new_vector = pygame.Vector2()
        for dist, fish in self.close_fish:
            new_vector += pygame.Vector2((fish.rect.x - self.rect.x), (fish.rect.y - self.rect.y))

        if new_vector.length_squared() > 0:
            new_vector = new_vector.normalize()

        self.vector = (self.vector + new_vector * dt * Setting.ALIGNMENT_STRENGTH).normalize()