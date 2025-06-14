import pygame, sys, random, math
from copy import deepcopy

random.seed(1)

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
