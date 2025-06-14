from parameter import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, vector, speed, dt):
        self.x += vector.x * speed * dt
        self.y += vector.y * speed * dt

    def get_pos(self):
        return self.x, self.y

    def draw(self, color):
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 3)