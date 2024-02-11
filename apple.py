#!/usr/bin/env python3
import os
import pygame
import random

from utils import clip

class Apple(pygame.sprite.Sprite):
    SCALE_FACTOR = 0.5 
    def __init__(self, cell_number: int, cell_size: int):
        pygame.sprite.Sprite.__init__(self)

        # load apple
        apple = pygame.image.load(os.path.join(os.getcwd(), "textures", "apple.png")).convert_alpha()
        self.image = pygame.transform.scale(clip(apple, 7, 3, 34, 36), ((cell_size) * Apple.SCALE_FACTOR, 
                                                           cell_size * Apple.SCALE_FACTOR))

        self.rect = self.image.get_rect()
        top_x = random.randint(0, (cell_number - 1)) * cell_size 
        top_y = random.randint(0, (cell_number - 1)) * cell_size 
        self.rect.center = (top_x + cell_size / 2, top_y + cell_size / 2)

        print(f"apple: {self.rect}")

    def update(self) -> None:
        pass