import pygame, sys, random
import numpy as np

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
fishConsideration = 6
clock = pygame.time.Clock()

#pygame.display.set_caption("Fish simulation")


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def position(self):
        return self.x, self.y

    def draw(self):
        pygame.draw.circle(screen, [255, 255, 255], (self.x, self.y), 3)

    def rotate_around(self, center, angle):
        """
        Tourne le point autour d'un centre d'un angle donné en degrés.
        """
        # Conversion en radians
        angle = np.radians(angle)
        cos_a, sin_a = np.cos(angle), np.sin(angle)

        # Décalage du point pour le recentrer sur (0,0)
        dx = self.x - center.x
        dy = self.y - center.y

        # Rotation
        new_x = dx * cos_a - dy * sin_a
        new_y = dx * sin_a + dy * cos_a

        # Retour au repère d'origine
        self.x = center.x + new_x
        self.y = center.y + new_y

class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def draw(self):
        pygame.draw.line(screen, (50, 50, 200), self.p1.position(), self.p2.position(), 7)


class Fish:
    def __init__(self):
        self.body = []
        self.center = Point(
            SCREEN_WIDTH / 2 + random.randint(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2),
            SCREEN_HEIGHT / 2 + random.randint(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
        )

        self.body.append(Point(self.center.x, self.center.y - 5))
        self.body.append(Point(self.center.x + 15, self.center.y))
        self.body.append(Point(self.center.x, self.center.y + 5))

        self.moving = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.moving /= np.linalg.norm(self.moving)  # Normalisation

        self.speed = 2  # Vitesse constante
        self.closer = []

    def move(self, x, y):
        self.center.move(x, y)
        for i in range(len(self.body)):
            self.body[i].move(x, y)

    def closerFish(self, fishList):
        self.closer.clear()
        attraction = np.array([0.0, 0.0])
        repulsion = np.array([0.0, 0.0])
        min_distance = 20  # Distance minimale avant répulsion

        for fish in fishList:
            if fish is not self:
                direction = np.array([fish.center.x - self.center.x, fish.center.y - self.center.y])
                distance = np.linalg.norm(direction)

                if distance > 0:  # Éviter la division par zéro
                    direction /= distance  # Normalisation

                    if distance < min_distance:
                        repulsion -= direction * (min_distance / distance)  # Répulsion
                    else:
                        attraction += direction  # Attraction

        # Appliquer les forces
        self.moving += attraction * 0.05  # Attraction faible
        self.moving += repulsion * 0.2  # Répulsion plus forte

        # Normalisation pour maintenir une vitesse constante
        norm = np.linalg.norm(self.moving)
        if norm > 0:
            self.moving = (self.moving / norm) * self.speed

    def bounce(self):
        if self.center.x <= 0 or self.center.x >= SCREEN_WIDTH:
            self.moving[0] *= -1
        if self.center.y <= 0 or self.center.y >= SCREEN_HEIGHT:
            self.moving[1] *= -1

        # Réapplique la vitesse constante
        self.moving = (self.moving / np.linalg.norm(self.moving)) * self.speed

    def getMove(self):
        return self.moving[0], self.moving[1]

    def pos(self):
        print(f"pos x : {self.center.x}, pos y : {self.center.y}")

    def draw(self):
        for i in range(len(self.body) - 1):
            s = Segment(self.body[i], self.body[i + 1])
            s.draw()
            self.body[i].draw()
        self.body[i + 1].draw()

    def update(self, fishList):
        self.closerFish(fishList)
        self.bounce()

        # Mise à jour de la position
        self.move(self.moving[0], self.moving[1])
        self.draw()


fish = []
for i in range(100):
    fish.append(Fish())

while True:
    screen.fill((0, 0, 0))  # Fond noir
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for i in range(len(fish)):
        fish[i].update(fish)

    pygame.display.flip()
    clock.tick(FPS)