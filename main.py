import pygame
import sys
import Setting
from ParameterWindow import ParameterWindow
import tkinter as tk
import threading

import Universe
#random.seed(1)

universe = Universe.Universe()

def open_param_window():
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale de Tkinter
    ParameterWindow(root)
    root.mainloop()

while True:
    Setting.screen.fill((0, 0, 0))

    dt = Setting.clock.tick(60) / 1000

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Clic droit
                threading.Thread(target=open_param_window, daemon=True).start()

    # Do something
    universe.update(dt)


    pygame.display.flip()
    Setting.clock.tick(Setting.FPS)
