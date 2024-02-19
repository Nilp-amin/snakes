#!/usr/bin/env python3
import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self,
                 cell_size,
                 grid_pos: pygame.Vector2):
        super().__init__()

        x, y = grid_pos
        self.rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)

    def get_grid_position(self) -> pygame.Vector2:
        x, y = self.rect.center
        return pygame.Vector2(int((x - self.cell_size / 2) / self.cell_size), 
                              int((y - self.cell_size / 2) / self.cell_size))

class Boundry(object):
    def __init__(self, 
                 collidable: pygame.sprite.Group, 
                 cell_number: int, 
                 cell_size: int):

        self.collidable = collidable

        # FIXME: combine the loops into one loop as they are identicle
        # add walls onto top and bottom row of map
        for x in range(cell_number):
            self.collidable.add(Wall(cell_size, pygame.Vector2(x, -1)))
            self.collidable.add(Wall(cell_size, pygame.Vector2(x, cell_number)))

        # add walls to far left and far right of map
        for y in range(cell_number):
            self.collidable.add(Wall(cell_size, pygame.Vector2(-1, y)))
            self.collidable.add(Wall(cell_size, pygame.Vector2(cell_number, y)))
