#!/usr/bin/env python3
import os
import pygame

from apple import Apple
from snake import SnakeChunk
from grid import Grid
from utils import clip

class World(object):
    ALLOWED_MOVES = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    def __init__(self, screen: pygame.display, cell_number: int, cell_size: int):
        # the game screen
        self._screen = screen
        self._cell_number = cell_number
        self._cell_size = cell_size

        # stores the body of the snake
        self._snake = pygame.sprite.Group() 
        # stores objects which cause collision
        self._collisions = pygame.sprite.Group() 
        # stores the objects which can be eaten 
        self.edible = pygame.sprite.GroupSingle(Apple(cell_number, cell_size))

        # queues the moves to be done in order
        self._move_queue = []
        # the world grid
        self.grid = pygame.sprite.Group()


        # add the grass onto the window
        for x_cell_number in range(self._cell_number):
            for y_cell_number in range(self._cell_number):
                grass = Grid(self._cell_size, 
                             self._cell_size * x_cell_number, 
                             self._cell_size * y_cell_number)
                self.grid.add(grass)

        # only have to draw the grid once
        self.grid.draw(self._screen)

    def add_move(self, key: int) -> None:
        if key in World.ALLOWED_MOVES:
            self._move_queue.append(key)

    def update(self, dt: float) -> None:
        self.edible.draw(self._screen)