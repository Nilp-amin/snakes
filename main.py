#!/usr/bin/env python3
import pygame

from world import World
from manager import ScoreManager 

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    cell_number = 15
    cell_size = 120 

    screen = pygame.display.set_mode((cell_number * cell_size, (cell_number * cell_size) + ScoreManager.SCORE_CARD_HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Snake")

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 100)
    clock = pygame.time.Clock()

    running = True
    dt = 0

    world = World(cell_number, cell_size)
    score_manager = ScoreManager(cell_number, cell_size)
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
                world.set_direction(event.key)
            if event.type == pygame.USEREVENT:
                # update the world on every time timer ticks 
                world_surface, score, deaths = world.update(dt)
                ui_surface = score_manager.update(score, deaths)

                screen.blit(world_surface, (0, 0))
                screen.blit(ui_surface, (0, cell_number * cell_size))

                # flip the display to show changes to screen
                pygame.display.flip()

        # Limit FPS to 60 and obtain dt for physics
        dt = clock.tick(60) / 1000