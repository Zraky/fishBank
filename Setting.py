import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1800, 1000
clock = pygame.time.Clock()
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


ALIGNMENT_STRENGTH = 10

nb_closer_fish = 7

spacing = 40
optimal_dist = 50
max_dist = 80

COHESION_WEIGHT = 0.2
ALIGNMENT_WEIGHT = 0.5
view_fish=400



pygame.display.set_caption('FishEvolve')
#icon = pygame.image.load()
#pygame.display.set_icon(icon)