#!/usr/bin/env python3
import os
import pygame

from world import World

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    cell_number = 15 
    cell_size = 40 
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    world = World(screen, cell_number, cell_size)
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
                world.add_move(event.key)

        # update the world on every tick
        world.update(dt)

        # flip the display to show changes to screen
        pygame.display.flip()

        # Limit FPS to 60 and obtain dt for physics
        dt = clock.tick(60) / 1000