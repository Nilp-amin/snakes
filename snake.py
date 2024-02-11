#!/usr/bin/env python3
from __future__ import annotations

from typing import Dict, Tuple

import os
import pygame

class SnakeChunk(pygame.sprite.Sprite):
    SCALE_FACTOR = 0.5
    def __init__(self, 
                 texture_map: Dict[Tuple[int, int], pygame.Surface],
                 cell_number: int, 
                 cell_size: int,
                 grid_pos: pygame.Vector2):
        pygame.sprite.Sprite.__init__(self)


        # correctly scale each of the textures once
        self.texture_map = dict()
        for key, texture in texture_map.items():
            self.texture_map[key] = pygame.transform.scale(texture, (cell_size * SnakeChunk.SCALE_FACTOR,
                                                                     cell_size * SnakeChunk.SCALE_FACTOR)) 

        # load snake default snake texture
        self.image = self.texture_map["default"]

        self.rect = self.image.get_rect()
        # TODO: make sure this is not the same position as the apple
        x, y = grid_pos
        top_x = x * cell_size 
        top_y = y * cell_size 
        self.rect.center = (top_x + cell_size / 2, top_y + cell_size / 2)

        self.cell_number = cell_number
        self.cell_size = cell_size

    def set_grid_position(self, position: pygame.Vector2) -> SnakeChunk:
        x, y = position
        top_x = x * self.cell_size 
        top_y = y * self.cell_size 
        self.rect.center = (top_x + self.cell_size / 2, top_y + self.cell_size / 2)

        return self

    def shift_grid_xy(self, shift: pygame.Vector2) -> SnakeChunk:
        self.image = self.texture_map[(int(shift.x), int(shift.y))]

        self.rect.x += (shift.x * self.cell_size)
        self.rect.y += (shift.y * self.cell_size)

        return self

    def get_grid_position(self) -> pygame.Vector2:
        # TODO: checkout pygame.Rect.move_ip()
        x, y = self.rect.center
        return pygame.Vector2((x - self.cell_size / 2) / self.cell_size, 
                              (y - self.cell_size / 2) / self.cell_size)

    def update(self) -> None:
        pass

class Snake(object):
    def __init__(self, cell_number: int, cell_size: int):

        # load texture map for snake tail
        self.tail_texture_map = {
            "default" : self.load_snake_texture("tail_left"),
            (1, 0) : self.load_snake_texture("tail_left"),
            (-1, 0) : self.load_snake_texture("tail_right"),
            (0, 1) : self.load_snake_texture("tail_up"),
            (0, -1) : self.load_snake_texture("tail_down")
        }

        # load texture map for snake body
        self.body_texture_map = {
            "default" : self.load_snake_texture("body_horizontal"),
            (1, 0) : self.load_snake_texture("body_horizontal"),
            (-1, 0) : self.load_snake_texture("body_horizontal"),
            (0, 1) : self.load_snake_texture("body_vertical"),
            (0, -1) : self.load_snake_texture("body_vertical")
        }

        # load texture map for snake head
        self.head_texture_map = {
            "default" : self.load_snake_texture("head_right"),
            (1, 0) : self.load_snake_texture("head_right"),
            (-1, 0) : self.load_snake_texture("head_left"),
            (0, 1) : self.load_snake_texture("head_down"),
            (0, -1) : self.load_snake_texture("head_up")
        }


        # the body of the snake
        self.chunks = pygame.sprite.Group(
            SnakeChunk(self.tail_texture_map, cell_number, cell_size, pygame.Vector2(2, 5)),
            SnakeChunk(self.body_texture_map, cell_number, cell_size, pygame.Vector2(3, 5)),
            SnakeChunk(self.head_texture_map, cell_number, cell_size, pygame.Vector2(4, 5))
        ) 

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

    def load_snake_texture(self, texture_name: str) -> pygame.Surface:
        return pygame.image.load(os.path.join(os.getcwd(), "textures", f"{texture_name}.png")).convert_alpha()

    def advance_snake(self, direction: int) -> None:
        # make sure the direction isn't 180 deg opposite to curr dir
        if self.current_direction is None:
            self.current_direction = direction 
        elif direction is not None and direction in self.valid_moves[self.current_direction]:
            self.current_direction = direction 

        if self.current_direction:
            snake_chunks = self.chunks.sprites()
            for i, snake_chunk in enumerate(self.chunks):
                chunk_shift = pygame.Vector2(0, 0) 
                if i == len(snake_chunks) - 1: # special case for the head of the snake
                    if self.current_direction == pygame.K_w:
                        chunk_shift = pygame.Vector2(0, -1)
                    elif self.current_direction == pygame.K_s:
                        chunk_shift = pygame.Vector2(0, 1)
                    elif self.current_direction == pygame.K_a:
                        chunk_shift = pygame.Vector2(-1, 0)
                    elif self.current_direction == pygame.K_d:
                        chunk_shift = pygame.Vector2(1, 0)
                else:
                    forward_snake_chunk = snake_chunks[i + 1]
                    chunk_shift = forward_snake_chunk.get_grid_position() - snake_chunk.get_grid_position() 

                snake_chunk.shift_grid_xy(chunk_shift)

    def draw(self, surface: pygame.Surface) -> None:
        self.chunks.draw(surface)