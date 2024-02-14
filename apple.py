#!/usr/bin/env python3
from __future__ import annotations

import os
import pygame
import random

from utils import clip

from typing import Set

class Apple(pygame.sprite.Sprite):
    SCALE_FACTOR = 0.5 
    def __init__(self, cell_number: int, cell_size: int):
        super().__init__()

        # load apple
        apple = pygame.image.load(os.path.join(os.getcwd(), "textures", "apple.png")).convert_alpha()
        self.image = pygame.transform.scale(clip(apple, 7, 3, 34, 36), ((cell_size) * Apple.SCALE_FACTOR, 
                                                           cell_size * Apple.SCALE_FACTOR))

        # TODO: make sure this is not the same position as the snake 
        self.rect = self.image.get_rect()
        top_x = random.randint(0, (cell_number - 1)) * cell_size 
        top_y = random.randint(0, (cell_number - 1)) * cell_size 
        self.rect.center = (top_x + cell_size / 2, top_y + cell_size / 2)

        self.cell_number = cell_number
        self.cell_size = cell_size

    def generate_random_position(self) -> pygame.Vector2:
        x = random.randint(0, (self.cell_number - 1)) * self.cell_size 
        y = random.randint(0, (self.cell_number - 1)) * self.cell_size 

        return pygame.Vector2(x, y)

    def set_grid_position(self, position: pygame.Vector2) -> Apple:
        x, y = position
        top_x = x * self.cell_size 
        top_y = y * self.cell_size 
        self.rect.center = (top_x + self.cell_size / 2, top_y + self.cell_size / 2)

        return self

    def set_random_position(self, invalid_positions: Set[pygame.Vector2]) -> Apple:
        random_position = self.generate_random_position()
        while set(random_position) & invalid_positions:
            random_position = self.generate_random_position()

        self.rect.center = (random_position.x + self.cell_size / 2, random_position.y + self.cell_size / 2)

        return self