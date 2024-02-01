#!/usr/bin/env python3
import os
import pygame

from utils import clip

class Grid(pygame.sprite.Sprite):
    def __init__(self, cell_size: int, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        # load in grass
        grasses = pygame.image.load(os.path.join(os.getcwd(), "textures", "grass.png"))
        grass = clip(grasses, 0, 0, 16, 16)

        self.image = pygame.transform.scale(grass, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y =y 

    def update(self, x: int, y: int) -> None:
        pass