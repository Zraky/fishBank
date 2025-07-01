import pygame
import math
import random
import Setting

class Fish(pygame.sprite.Sprite):
    def __init__(self, id, speed, color, rect, vector=None, refresh=0):
        super().__init__()
        self.id = id
        self.speed = speed
        self.color = color
        self.rect = rect
        if vector is None:
            vector = (random.uniform(-1, 1), random.uniform(-1, 1))
        self.vector = pygame.Vector2(vector).normalize()
        self.close_fish = []
        self.radius = (self.rect.height + self.rect.width) / 2
        self.refresh_wait = int(refresh)

    def update_move(self, fishs, dt):
        self.close_fish.clear()
        arround_fish = []
        view_fish = []

        for fish in fishs:
            if fish.id == self.id:
                continue

            dist = pygame.Vector2(self.rect.center).distance_to(fish.rect.center)

            # --- Liste des poissons proches pour attraction/répulsion
            if dist < Setting.max_dist:
                if len(arround_fish) < Setting.nb_closer_fish:
                    arround_fish.append((dist, fish))
                else:
                    arround_fish.sort(key=lambda x: x[0])
                    if dist < arround_fish[-1][0]:
                        arround_fish[-1] = (dist, fish)

            # --- Champ de vision pour alignement
            if dist < Setting.view_fish:
                vec_to_fish = pygame.Vector2(fish.rect.center) - pygame.Vector2(self.rect.center)
                if vec_to_fish.length_squared() > 0:
                    vec_to_fish.normalize_ip()
                    angle_diff = self.vector.angle_to(vec_to_fish)
                    if -15 < angle_diff < 15:
                        view_fish.append(fish)

        # === Calcul des forces ===
        separation = pygame.Vector2()
        cohesion = pygame.Vector2()
        alignment = pygame.Vector2()

        for dist, fish in arround_fish:
            offset = pygame.Vector2(self.rect.center) - pygame.Vector2(fish.rect.center)
            if offset.length_squared() > 0:
                offset.normalize_ip()
            force = self.move_calcul(dist)
            cohesion += fish.vector * force
            self.close_fish.append((dist, fish))

        for fish in view_fish:
            alignment += fish.vector
            self.close_fish.append((0, fish))

        if cohesion.length_squared() > 0:
            cohesion = cohesion.normalize()
        if alignment.length_squared() > 0:
            alignment = alignment.normalize()

        final_vector = self.vector + (
                cohesion * Setting.COHESION_WEIGHT +
                alignment * Setting.ALIGNMENT_WEIGHT
        )

        if final_vector.length_squared() > 0:
            self.vector = final_vector.normalize()

    def move_calcul(self, dist):
        if dist < 1e-5 or dist >= Setting.max_dist:
            return 0
        if dist < Setting.spacing:
            return -(1 / dist) * (1 / Setting.spacing)
        else:
            return (1 / dist) * (1 / Setting.optimal_dist)

    def flee(self, fishs, dt):
        new_vec = pygame.Vector2()
        for fish in fishs:
            if fish.id == self.id:
                continue

            dist = pygame.Vector2(self.rect.center).distance_to(fish.rect.center)

            if dist < Setting.max_dist:
                offset = pygame.Vector2(self.rect.center) - pygame.Vector2(fish.rect.center)
                new_vec -= offset
                if dist < Setting.optimal_dist:
                    self.vector = self.vector - offset
                    if dist < Setting.spacing:
                        self.vector = self.vector - offset
                    self.vector.normalize()

            if new_vec.length_squared() > 0:
                new_vec.normalize()

            self.vector = (self.vector - new_vec).normalize()

    def move(self, dt):
        self.rect.x += self.vector.x * self.speed * dt
        self.rect.y += self.vector.y * self.speed * dt

    def draw(self, color):
        pygame.draw.circle(Setting.screen, color, self.rect.center, self.radius)

    def update(self, fishs, shark, dt):
        self.refesh(fishs, shark, dt)
        self.move(dt)

    def refesh(self, fishs, sharks, dt):
            if (Setting.refresh <= self.refresh_wait):
                self.update_move(fishs, dt)
                self.flee(sharks, dt)
                self.refresh_wait = 0

            else:
                self.refresh_wait += 1

def update_move_1(self, fishs, dt):
    # movement by count
    self.close_fish.clear()

    for fish in fishs:
        if fish.id == self.id:
            continue

        dist = pygame.Vector2(self.rect.center).distance_to(fish.rect.center)

        if len(self.close_fish) < Setting.nb_closer_fish:
            self.close_fish.append((dist, fish))
        else:
            self.close_fish.sort(key=lambda x: x[0])
            if dist < self.close_fish[-1][0]:
                self.close_fish[-1] = (dist, fish)

    new_vector = pygame.Vector2()
    for dist, fish in self.close_fish:
        new_vector += fish.vector

    if new_vector.length_squared() > 0:
        new_vector = new_vector.normalize()

    self.vector = (self.vector + new_vector * dt * Setting.ALIGNMENT_STRENGTH).normalize()

def update_move_2(self, fishs, dt):
    # movement by distance
    self.close_fish.clear()

    for fish in fishs:
        if fish.id == self.id:
            continue

        dist = pygame.Vector2(self.rect.center).distance_to(fish.rect.center)
        if dist >= Setting.max_dist:
            continue
        self.close_fish.append((dist, fish))

    new_vector = pygame.Vector2()
    for dist, fish in self.close_fish:
        new_vector += fish.vector

    if new_vector.length_squared() > 0:
        new_vector = new_vector.normalize()

    self.vector = (self.vector + new_vector * dt * Setting.ALIGNMENT_STRENGTH).normalize()

def update_move_3(self, fishs, dt):
    # movement by view
    self.close_fish.clear()

    angle = self.vector.angle_to((0, 0))
    for fish in fishs:
        if fish.id == self.id:
            continue

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
