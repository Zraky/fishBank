import pygame, sys, random, math
from copy import deepcopy

random.seed(1)

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

FPS = 0
NB_FISHS = 100
NB_SHARK = 5
SPEED = 200
REFRESH = 0

# by nb
NB_CLOSER_FISHES = 10

# by distance
DECAY_RATE = 0.05

DECAY_RATE_SHARK = 1
SHARK_RADIUS = 50



def draw_circle(fishs, name):
    reference_fish = None

    # Vérifier que name est un index valide
    for fish in fishs:
        if fish.name == name:
            reference_fish = fish
            break

    if reference_fish is None:
        return  # Si le poisson n'existe pas, on ne fait rien

    for fish in fishs:
        if fish is reference_fish:
            continue  # Ne pas comparer un poisson avec lui-même

        dist = math.hypot(reference_fish.center.x - fish.center.x, reference_fish.center.y - fish.center.y)

        if dist < 1:
            dist = 1  # Éviter la division par zéro

        intensity = max(0, 255 - (dist * 10))  # Ajustement du dégradé (modifiable selon besoin)

        pygame.draw.line(
            screen,
            (intensity, intensity, intensity),
            reference_fish.center.get_pos(),
            fish.center.get_pos(),
            2
        )


def draw_line(fishs, name=None, level=0):
    if (name == None):
        for i, fish in enumerate(fishs):
            for j in range(len(fish.close_fish)):
                pygame.draw.line(screen, (255, 0, 0), fish.center.get_pos(), fish.close_fish[j].center.get_pos(), 2)

    else:
        for i in range(len(fishs)):
            if (name == fishs[i].name):
                for j in range(len(fishs[i].close_fish)):
                    pygame.draw.line(screen, (0, 0, 255), fishs[i].center.get_pos(),
                                     fishs[i].close_fish[j].center.get_pos(), 2)


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


class Fish:
    def __init__(self, name, x, y, refresh=(0, 0), speed=None):
        self.name = name
        self.center = Point(x, y)
        self.vector = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.vector.length() > 0:
            self.vector = self.vector.normalize()
        self.refresh_time, self.refresh_wait = refresh
        self.speed = speed if speed else random.randint(SPEED // 2, SPEED)
        self.bank_move = pygame.math.Vector2(0, 0)

        self.close_fish = []

    def closerFish(self, fishList):
        self.bank_move = pygame.math.Vector2(0, 0)

        fishList = sorted(fishList, key=lambda f: math.hypot(self.center.x - f.center.x, self.center.y - f.center.y))
        self.close_fish.clear()
        for fish in fishList[1:NB_CLOSER_FISHES]:
            self.bank_move += fish.vector
            self.close_fish.append(fish)

        if self.bank_move.length() > 0:
            bank_move = self.bank_move.normalize() * 0.1
            self.vector += bank_move

        if self.vector.length() > 0:
            self.vector = self.vector.normalize()

    def bounce(self):
        if self.center.x <= 0:
            self.center.x = 0
            self.vector = pygame.math.Vector2(- self.vector.x, self.vector.y)

        elif self.center.x >= SCREEN_WIDTH:
            self.center.x = SCREEN_WIDTH
            self.vector = pygame.math.Vector2(- self.vector.x, self.vector.y)

        if self.center.y <= 0:
            self.center.y = 0
            self.vector = pygame.math.Vector2(self.vector.x, - self.vector.y)

        if self.center.y >= SCREEN_HEIGHT:
            self.center.y = SCREEN_HEIGHT
            self.vector = pygame.math.Vector2(self.vector.x, - self.vector.y)

    def move(self, dt):
        self.center.move(self.vector, self.speed, dt)

    def draw(self):
        self.center.draw((100, 255, 255))

    def fish_dist(self, other):
        return math.hypot(self.center.x - other.center.x, self.center.y - other.center.y)

    def refesh(self, fishs, sharks):
        if (self.refresh_time == self.refresh_wait):
            self.closerFish(fishs)
            self.flee_shark(sharks)
            self.refresh_wait = 0

        else:
            self.refresh_wait += 1

    def update(self, fishs, sharks, dt):
        self.refesh(fishs, sharks)
        self.bounce()
        self.move(dt)
        self.draw()

    def flee_shark(self, sharkList):
        for fish in sharkList:
            dist = self.fish_dist(fish)
            if dist < SHARK_RADIUS:
                self.vector += pygame.Vector2(self.center.x - fish.center.x,
                                              self.center.y - fish.center.y).normalize() * (1 - 1 / dist)
            self.vector = self.vector.normalize()


class Fishier(Fish):
    def __init__(self, name, x, y, refresh=(0, 0), speed=None):
        Fish.__init__(self, name, x, y, refresh, speed)

    def closerFish(self, fishList):
        self.bank_move = pygame.math.Vector2(0, 0)

        for fish in fishList[1:]:
            dist = self.fish_dist(fish)
            self.bank_move += fish.vector * math.exp(-DECAY_RATE * dist)

        if self.bank_move.length() > 0:
            self.bank_move = self.bank_move.normalize()
            self.vector += self.bank_move

        if self.vector.length() > 0:
            self.vector = self.vector.normalize()

        if self.bank_move.length() > 0:
            bank_move = self.bank_move.normalize()
            self.vector += bank_move

        if self.vector.length() > 0:
            self.vector = self.vector.normalize()

    def bounce(self):
        if self.center.x <= 0:
            self.center.x = SCREEN_WIDTH

        elif self.center.x >= SCREEN_WIDTH:
            self.center.x = 0

        if self.center.y <= 0:
            self.center.y = SCREEN_HEIGHT


        elif self.center.y >= SCREEN_HEIGHT:
            self.center.y = 0


class Shark(Fish):
    def __init__(self, name, x, y, refresh=(0, 0), speed=None):
        Fish.__init__(self, name, x, y, refresh, speed)

    def closerFish(self, fishList):
        self.bank_move = pygame.math.Vector2(0, 0)

        fishList = sorted(fishList, key=lambda f: math.hypot(self.center.x - f.center.x, self.center.y - f.center.y))

        fishList.remove(fishList[0])

        self.vector = pygame.Vector2(fishList[0].center.x - self.center.x,
                                     fishList[0].center.y - self.center.y).normalize()

        if self.vector.length() > 0:
            self.vector = self.vector.normalize()

    def bounce(self):
        if self.center.x <= 0:
            self.center.x += SCREEN_WIDTH

        elif self.center.x >= SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH

        if self.center.y <= 0:
            self.center.y += SCREEN_HEIGHT

        if self.center.y >= SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT

    def draw(self):
        self.center.draw((255, 0, 0))

    def refesh(self, fishs, sharks):
        if (self.refresh_time == self.refresh_wait):
            self.closerFish(fishs)
            self.refresh_wait = 0
        else:
            self.refresh_wait += 1

    def eating(self, fish):
        dist = 100
        if (self.center.x - fish.center.x <= dist and self.center.y - fish.center.y <=dist):
            return True
        return False


fishs = []

for i in range(1, NB_FISHS + 1):
    fishs.append(Fishier(i, random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
                         (REFRESH, (REFRESH % i))))

sharks = []
for i in range(1, NB_SHARK + 1):
    sharks.append(Shark(i, random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
                        (REFRESH, (REFRESH % i))))

police = pygame.font.SysFont(None, 40)

while True:
    dt = clock.tick(FPS) / 1000
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    for i, fish in enumerate(fishs):
        fish.update(fishs, sharks, dt)

    for i, shark in enumerate(sharks):
        shark.update(fishs, sharks, dt)

    # draw_circle(fishs, 1)

    draw_line(fishs)
    # draw_line(fishs, 1)
    game_credit_text_1 = police.render("FPS : " + str(clock.get_fps()), True, (200, 200, 200))
    screen.blit(game_credit_text_1, (0, 0))

    pygame.display.flip()

