#!/usr/bin/env python3
import os
import pygame
import random

from utils import clip

class SnakeChunk(pygame.sprite.Sprite):
    SCALE_FACTOR = 0.5
    def __init__(self, 
                 texture_name: str, 
                 cell_number: int, 
                 cell_size: int,
                 cell_x: int,
                 cell_y: int):
        pygame.sprite.Sprite.__init__(self)

        # load snake body
        snake_chunk = pygame.image.load(os.path.join(os.getcwd(), "textures", f"{texture_name}.png")).convert_alpha()
        self.image = pygame.transform.scale(snake_chunk, ((cell_size) * SnakeChunk.SCALE_FACTOR, 
                                                           cell_size * SnakeChunk.SCALE_FACTOR))

        self.rect = self.image.get_rect()
        # TODO: make sure this is not the same position as the apple
        top_x = cell_x * cell_size 
        top_y = cell_y * cell_size 
        self.rect.center = (top_x + cell_size / 2, top_y + cell_size / 2)
        self.rect.width = cell_size
        self.rect.height = cell_size

    def update(self) -> None:
        pass

class Snake(object):
    def __init__(self, cell_number: int, cell_size: int):
        # the body of the snake
        self.body = pygame.sprite.Group(SnakeChunk("tail_left", 
                                                     cell_number, 
                                                     cell_size,
                                                     2, 5),
                                        SnakeChunk("head_right", 
                                                     cell_number, 
                                                     cell_size,
                                                     3, 5)) 

        # the current direction of the head
        self.current_direction = None

        # the current valid move given the current snake head direction
        self.valid_moves = {
            pygame.K_w : [pygame.K_a, pygame.K_d],
            pygame.K_s : [pygame.K_a, pygame.K_d],
            pygame.K_a : [pygame.K_w, pygame.K_s],
            pygame.K_d : [pygame.K_w, pygame.K_s]
        }

        self.cell_number = cell_number
        self.cell_size = cell_size

    def advance_snake(self, direction: int) -> None:
        # make sure the direction isn't 180 deg opposite to curr dir
        if self.current_direction is None:
            self.current_direction = direction 
        elif direction is not None and direction in self.valid_moves[self.current_direction]:
            self.current_direction = direction 

        if self.current_direction:
            snake_chunks = self.body.sprites()
            for i, snake_chunk in enumerate(self.body):
                if i == len(snake_chunks) - 1: # special case for the head of the snake
                    if self.current_direction == pygame.K_w:
                        snake_chunk.rect.y -= self.cell_size
                    elif self.current_direction == pygame.K_s:
                        snake_chunk.rect.y += self.cell_size
                    elif self.current_direction == pygame.K_a:
                        snake_chunk.rect.x -= self.cell_size
                    elif self.current_direction == pygame.K_d:
                        snake_chunk.rect.x += self.cell_size
                else:
                    forward_snake_chunk = snake_chunks[i + 1]
                    snake_chunk.rect.x = forward_snake_chunk.rect.x
                    snake_chunk.rect.y = forward_snake_chunk.rect.y

    def draw(self, surface: pygame.Surface) -> None:
        self.body.draw(surface)