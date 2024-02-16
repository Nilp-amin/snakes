#!/usr/bin/env python3
import pygame

from manager import ScoreManager 
from world import World

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    cell_number = 15
    cell_size = 120 

    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size), pygame.SCALED)
    pygame.display.set_caption("Snake")

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 100)
    clock = pygame.time.Clock()

    running = True
    dt = 0

    world = World(screen, cell_number, cell_size)
    score_manager = ScoreManager(screen, cell_number, cell_size)
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
                world.add_move(event.key)
            if event.type == pygame.USEREVENT:
                # update the world on every time timer ticks 
                update_score = world.update(dt)
                score_manager.update(update_score)

        # flip the display to show changes to screen
        pygame.display.flip()

        # Limit FPS to 60 and obtain dt for physics
        dt = clock.tick(60) / 1000