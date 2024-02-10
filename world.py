#!/usr/bin/env python3
import pygame

from apple import Apple
from snake import SnakeChunk

from collections import deque

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
        self.snake = pygame.sprite.Group(SnakeChunk("tail_left", 
                                                     cell_number, 
                                                     cell_size,
                                                     2, 5),
                                        SnakeChunk("head_right", 
                                                     cell_number, 
                                                     cell_size,
                                                     3, 5)) 
        # stores objects which cause collision
        self._collisions = pygame.sprite.Group() 
        # stores the objects which can be eaten 
        self.edible = pygame.sprite.GroupSingle(Apple(cell_number, cell_size))

        # queues the moves to be done in order
        self.move_queue = deque([]) 

        # keep track of the current direction of the head
        self.curr_snake_dir = None

        self.valid_moves = {
            pygame.K_w : [pygame.K_a, pygame.K_d],
            pygame.K_s : [pygame.K_a, pygame.K_d],
            pygame.K_a : [pygame.K_w, pygame.K_s],
            pygame.K_d : [pygame.K_w, pygame.K_s]
        }


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

    def advance_snake(self, dir: int = None) -> None:
        # make sure the direction isn't 180 deg opposite to curr dir
        if self.curr_snake_dir is None:
            self.curr_snake_dir = dir
        elif dir is not None and dir in self.valid_moves[self.curr_snake_dir]:
            self.curr_snake_dir = dir

        if self.curr_snake_dir:
            snake_chunks = self.snake.sprites()
            for i, snake_chunk in enumerate(self.snake):
                if i == len(snake_chunks) - 1: # special case for the head of the snake
                    if self.curr_snake_dir == pygame.K_w:
                        snake_chunk.rect.y -= self.cell_size
                    elif self.curr_snake_dir == pygame.K_s:
                        snake_chunk.rect.y += self.cell_size
                    elif self.curr_snake_dir == pygame.K_a:
                        snake_chunk.rect.x -= self.cell_size
                    elif self.curr_snake_dir == pygame.K_d:
                        snake_chunk.rect.x += self.cell_size
                else:
                    forward_snake_chunk = snake_chunks[i + 1]
                    snake_chunk.rect.x = forward_snake_chunk.rect.x
                    snake_chunk.rect.y = forward_snake_chunk.rect.y

    def update(self, dt: float) -> None:
        key = None
        if self.move_queue:
            key = self.move_queue.popleft()

        self.advance_snake(key)

        self.draw_background()
        self.edible.draw(self._screen)
        self.snake.draw(self._screen)