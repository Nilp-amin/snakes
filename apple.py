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
        apple = pygame.image.load(os.path.join(os.getcwd(), "textures", "apple.png"))
        cliped_apple = clip(apple, 24, 19, 16, 18)
        self.image = pygame.transform.scale(cliped_apple, ((cell_size - 2) * Apple.SCALE_FACTOR, 
                                                           cell_size * Apple.SCALE_FACTOR))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, (cell_number - 1) * cell_size) 
        self.rect.y = random.randint(0, (cell_number - 1) * cell_size) 

    def update(self) -> None:
        pass