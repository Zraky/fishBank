from parameter import *
from fish.fish import *
from fish.variant.Shark import Shark

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

"""
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
"""

fishs = []

for i in range(1, NB_FISHS + 1):
    fishs.append(Fish(i, random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
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

    # draw_line(fishs, 1)
    game_credit_text_1 = police.render("FPS : " + str(clock.get_fps()), True, (200, 200, 200))
    screen.blit(game_credit_text_1, (0, 0))

    pygame.display.flip()

