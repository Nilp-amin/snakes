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