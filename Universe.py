import random

import pygame.rect
import Setting
import Fish
import Shark



class Universe:
    def __init__(self):
        self.all_fish = []
        x = random.randint(0, Setting.SCREEN_WIDTH)
        y = random.randint(0, Setting.SCREEN_HEIGHT)
        rect = pygame.Rect(x, y, 2, 2)
        fish = Fish.Fish(0, 400, (150, 150, 255), rect)
        self.all_fish.append(fish)
        for i in range(1, 100):
            x = random.randint(0, Setting.SCREEN_WIDTH)
            y = random.randint(0, Setting.SCREEN_HEIGHT)
            rect = pygame.Rect(x, y, 2, 2)
            fish = Fish.Fish(i, 400, (150, 150, 255), rect, refresh=(i % Setting.refresh))
            self.all_fish.append(fish)

        self.all_shark = []
        for i in range(10):
            x = random.randint(0, Setting.SCREEN_WIDTH)
            y = random.randint(0, Setting.SCREEN_HEIGHT)
            rect = pygame.Rect(x, y, 2, 2)
            shark = Shark.Shark(i, 400, (255, 150, 150), rect, refresh=(i % Setting.refresh))
            self.all_shark.append(shark)

    def draw_link(self, fish, color):
        for dist, fish_close in fish.close_fish:
            pygame.draw.line(Setting.screen, color, fish.rect.center, fish_close.rect.center, 2)

    def bounce(self, fish):
        if fish.rect.centerx < 0:
            fish.rect.centerx = Setting.SCREEN_WIDTH

        elif fish.rect.centerx > Setting.SCREEN_WIDTH:
            fish.rect.centerx = 0

        if fish.rect.centery < 0:
            fish.rect.centery = Setting.SCREEN_HEIGHT

        elif fish.rect.centery > Setting.SCREEN_HEIGHT:
            fish.rect.centery = 0

    def bounce_shark(self, fish):
        margin = 10
        bounce_strength = 0.5

        if fish.rect.left <= margin:
            fish.vector.x = abs(fish.vector.x) * bounce_strength
        elif fish.rect.right >= Setting.SCREEN_WIDTH - margin:
            fish.vector.x = -abs(fish.vector.x) * bounce_strength

        if fish.rect.top <= margin:
            fish.vector.y = abs(fish.vector.y) * bounce_strength
        elif fish.rect.bottom >= Setting.SCREEN_HEIGHT - margin:
            fish.vector.y = -abs(fish.vector.y) * bounce_strength

        # Re-normalisation
        if fish.vector.length_squared() > 0:
            fish.vector.normalize_ip()

    def invers_coef(self, value, max_value) -> int:
        if value == 0 or max_value == 0:
            return 0
        return value / max_value

    def update(self, dt):
        prev_all_fish = self.all_fish.copy()
        prev_all_shark = self.all_shark.copy()
        for fish in self.all_fish:
            self.bounce(fish)
            fish.update(prev_all_fish, prev_all_shark, dt)
            fish.draw(fish.color)
            if fish.id in Setting.display_fish_link:
               self.draw_link(fish, (255, 255, 255))

        for fish in self.all_shark:
            self.bounce_shark(fish)
            fish.update(prev_all_fish, prev_all_shark, dt)

            if Setting.display_shark:
                fish.draw(fish.color)

            if fish.id in Setting.display_shark_link:
                self.draw_link(fish, (255, 155, 155))
