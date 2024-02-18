#!/usr/bin/env python3
import pygame

from manager import ScoreManager 
from world import World

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    cell_number = 15
    cell_size = 120 
    score_card_height = 100

    screen = pygame.display.set_mode((cell_number * cell_size, (cell_number * cell_size) + score_card_height), pygame.SCALED)
    pygame.display.set_caption("Snake")

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 100)
    clock = pygame.time.Clock()

    running = True
    dt = 0

    # set a surface for the actual game
    world_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size), pygame.SCALED)
    # set a surface for the UI
    ui_surface = pygame.Surface((cell_number * cell_size, score_card_height), pygame.SCALED)

    world = World(world_surface, cell_number, cell_size)
    score_manager = ScoreManager(ui_surface, cell_number, cell_size)
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
                world.set_direction(event.key)
            if event.type == pygame.USEREVENT:
                # update the world on every time timer ticks 
                score, deaths = world.update(dt)
                score_manager.update(score, deaths)

        # flip the display to show changes to screen
        screen.blit(world_surface, (0, 0))
        screen.blit(ui_surface, (0, cell_number * cell_size))
        pygame.display.flip()

        # Limit FPS to 60 and obtain dt for physics
        dt = clock.tick(60) / 1000