import random

from Setting import *
import Universe

#random.seed(1)

# Provide initial species, prey, and detection radius

universe = Universe.Universe()

while True:
    screen.fill((0, 0, 0))  # Clear screen with black

    dt = clock.tick(60) / 1000

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Do something
    universe.update(dt)

    #print(1/dt)

    pygame.display.flip()
    clock.tick(FPS)
