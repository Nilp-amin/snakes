#!/usr/bin/env python3
import pygame

from apple import Apple
from snake import SnakeChunk
from grid import Grid

class World(object):
    ALLOWED_MOVES = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    BACKGROUND_COLOUR = (175, 215, 70)
    GRASS_COLOUR = (167, 209, 61)
    def __init__(self, screen: pygame.display, cell_number: int, cell_size: int):
        # the game screen
        self._screen = screen
        self.cell_number = cell_number
        self.cell_size = cell_size

        # stores the body of the snake
        self.snake = pygame.sprite.Group(SnakeChunk("head_right", 
                                                     cell_number, 
                                                     cell_size,
                                                     3, 5),
                                        SnakeChunk("tail_left", 
                                                     cell_number, 
                                                     cell_size,
                                                     2, 5)) 
        # stores objects which cause collision
        self._collisions = pygame.sprite.Group() 
        # stores the objects which can be eaten 
        self.edible = pygame.sprite.GroupSingle(Apple(cell_number, cell_size))

        # queues the moves to be done in order
        self.move_queue = []


    def add_move(self, key: int) -> None:
        if key in World.ALLOWED_MOVES:
            self.move_queue.append(key)

    def draw_background(self) -> None:
        # set background colour of world 
        self._screen.fill(World.BACKGROUND_COLOUR)

        # set alternating grass pattern
        for row in range(self.cell_number):
            for col in range(self.cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(row * self.cell_size, col * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self._screen, World.GRASS_COLOUR, grass_rect)
        pass

    def update(self, dt: float) -> None:
        if self.move_queue:
            key = self.move_queue.pop(0)
            if key == pygame.K_w:
                pass
            elif key == pygame.K_s:
                pass
            elif key == pygame.K_a:
                pass
            elif key == pygame.K_d:
                for snake_chunk in self.snake:
                    snake_chunk.rect.x += self.cell_size 
                pass
        else:
            # TODO: add logic to keep going in direction which head is pointing
            pass

        self.draw_background()
        self.edible.draw(self._screen)
        self.snake.draw(self._screen)