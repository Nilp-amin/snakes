#!/usr/bin/env python3
from __future__ import annotations

from typing import List, Dict, Tuple

import os
import pygame

class SnakeChunk(pygame.sprite.Sprite):
    SCALE_FACTOR = 1.0
    def __init__(self, 
                 texture_map: Dict[Tuple[int, int], pygame.Surface],
                 cell_number: int, 
                 cell_size: int,
                 grid_pos: pygame.Vector2):
        super().__init__()

        # correctly scale each of the textures once
        self.texture_map = dict()
        for key, texture in texture_map.items():
            self.texture_map[key] = pygame.transform.scale(texture, (cell_size * SnakeChunk.SCALE_FACTOR,
                                                                     cell_size * SnakeChunk.SCALE_FACTOR)) 

        # load snake default snake texture
        self.image = self.texture_map["default"]

        self.rect = self.image.get_rect()
        x, y = grid_pos
        top_x = x * cell_size 
        top_y = y * cell_size 
        self.rect.center = (top_x + cell_size / 2, top_y + cell_size / 2)

        self.cell_number = cell_number
        self.cell_size = cell_size

    def get_grid_position(self) -> pygame.Vector2:
        # TODO: checkout pygame.Rect.move_ip()
        x, y = self.rect.center
        return pygame.Vector2(int((x - self.cell_size / 2) / self.cell_size), 
                              int((y - self.cell_size / 2) / self.cell_size))

    def set_grid_position(self, position: pygame.Vector2) -> SnakeChunk:
        x, y = position
        top_x = x * self.cell_size 
        top_y = y * self.cell_size 
        self.rect.center = (top_x + self.cell_size / 2, top_y + self.cell_size / 2)

        return self

    def shift_grid_xy(self, shift: pygame.Vector2) -> SnakeChunk:
        raise NotImplementedError

    def set_texture(self, shift: pygame.Vector2) -> SnakeChunk:
        raise NotImplementedError

class Head(SnakeChunk):
    def __init__(self, 
                 texture_map: Dict[Tuple[int, int], pygame.Surface],
                 cell_number: int, 
                 cell_size: int,
                 grid_pos: pygame.Vector2):
        super().__init__(texture_map, cell_number, cell_size, grid_pos)

    def shift_grid_xy(self, shift: pygame.Vector2) -> SnakeChunk:
        self.rect.x += (shift.x * self.cell_size)
        self.rect.y += (shift.y * self.cell_size)

        return self

    def set_texture(self, shift: pygame.Vector2) -> SnakeChunk:
        self.image = self.texture_map[tuple(shift)]
        return self

class Body(SnakeChunk):
    def __init__(self, 
                 texture_map: Dict[Tuple[int, int], pygame.Surface],
                 cell_number: int, 
                 cell_size: int,
                 grid_pos: pygame.Vector2):
        super().__init__(texture_map, cell_number, cell_size, grid_pos)

        # the previous position in the grid of this chunk
        self.prev_grid_position = grid_pos 

    def shift_grid_xy(self, shift: pygame.Vector2) -> SnakeChunk:
        self.prev_grid_position = self.get_grid_position()
        self.rect.x += (shift.x * self.cell_size)
        self.rect.y += (shift.y * self.cell_size)

        return self

    def get_previous_grid_position(self) -> pygame.Vector2:
        return self.prev_grid_position

    def set_previous_grid_position(self, grid_pos: pygame.Vector2) -> None:
        self.prev_grid_position = grid_pos

    def set_texture(self, shift: pygame.Vector2) -> SnakeChunk:
        previous_shift = self.get_grid_position() - self.prev_grid_position
        if previous_shift != shift:
            # makes sure the correct texture for the given symmetry is used
            if abs(previous_shift.x) == 1:
                total_shift = previous_shift + shift
            elif abs(previous_shift.y) == 1:
                total_shift = -previous_shift - shift
        else:
            total_shift = shift 

        self.image = self.texture_map[tuple(total_shift)]

        return self


class Tail(SnakeChunk):
    def __init__(self, 
                 texture_map: Dict[Tuple[int, int], pygame.Surface],
                 cell_number: int, 
                 cell_size: int,
                 grid_pos: pygame.Vector2):
        super().__init__(texture_map, cell_number, cell_size, grid_pos)

    def shift_grid_xy(self, shift: pygame.Vector2) -> SnakeChunk:
        self.rect.x += (shift.x * self.cell_size)
        self.rect.y += (shift.y * self.cell_size)

        return self

    def set_texture(self, shift: pygame.Vector2) -> SnakeChunk:
        self.image = self.texture_map[tuple(shift)]
        return self

class Snake(object):
    def __init__(self, 
                 collidable: pygame.sprite.Group, 
                 cell_number: int, 
                 cell_size: int):
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
            (0, -1) : self.load_snake_texture("body_vertical"),
            (1, -1) : self.load_snake_texture("body_topleft"),
            (1, 1) : self.load_snake_texture("body_bottomleft"),
            (-1, -1) : self.load_snake_texture("body_topright"),
            (-1, 1) : self.load_snake_texture("body_bottomright")
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
        self.chunks = [ 
            Head(self.head_texture_map, cell_number, cell_size, pygame.Vector2(5, 5)),
            Body(self.body_texture_map, cell_number, cell_size, pygame.Vector2(4, 5)),
            Tail(self.tail_texture_map, cell_number, cell_size, pygame.Vector2(3, 5))
        ]

        self.chunks_group = pygame.sprite.Group(self.chunks)

        # the current valid move given the current snake head direction
        self.valid_moves = {
            pygame.K_w : [pygame.K_a, pygame.K_d],
            pygame.K_s : [pygame.K_a, pygame.K_d],
            pygame.K_a : [pygame.K_w, pygame.K_s],
            pygame.K_d : [pygame.K_w, pygame.K_s]
        }

        # the shift in grid position given a key input
        self.key_shift_map = {
            pygame.K_w : pygame.Vector2(0, -1),
            pygame.K_s : pygame.Vector2(0, 1),
            pygame.K_a : pygame.Vector2(-1, 0),
            pygame.K_d : pygame.Vector2(1, 0)
        }

        self.cell_number = cell_number
        self.cell_size = cell_size
        self.collidable = collidable

        # add snake chunks to colliadable
        self.collidable.add(self.chunks[1:])

        # the current direction of the head
        self.current_direction = None

    def get_head(self) -> Head:
        return self.chunks[0]

    def get_chunks(self) -> List[SnakeChunk]:
        return self.chunks

    def load_snake_texture(self, texture_name: str) -> pygame.Surface:
        return pygame.image.load(os.path.join(os.getcwd(), "textures", f"{texture_name}.png")).convert_alpha()

    def advance_snake(self, direction: int, add_chunk: bool = False) -> None:
        # FIXME: check key_shift_map for very first move as well...not allow it to go on itself
        # make sure the direction isn't 180 deg opposite to curr dir
        if self.current_direction is None:
            self.current_direction = direction 
        elif direction is not None and direction in self.valid_moves[self.current_direction]:
            self.current_direction = direction 

        if self.current_direction:
            chunks = self.chunks

            # make sure the current number of chunks are updated based on if a chunk needs to be added or not 
            if add_chunk:
                self.increase_size()
                chunks = self.chunks[:2]

            # TODO: combines these two for loops into a single for loop 
            # first move chunks only
            head_shift = self.key_shift_map[self.current_direction]
            old_forward_chunk_pos = pygame.Vector2(0, 0)
            for i, snake_chunk in enumerate(chunks):
                chunk_shift = pygame.Vector2(0, 0) 

                if i == 0:
                    chunk_shift = head_shift
                else:
                    chunk_shift = old_forward_chunk_pos - snake_chunk.get_grid_position() 

                old_forward_chunk_pos = snake_chunk.get_grid_position()
                snake_chunk.shift_grid_xy(chunk_shift)

            # now correct chunk textures
            forward_chunk_pos = pygame.Vector2(0, 0)
            for i, snake_chunk in enumerate(chunks):
                if i == 0:
                    snake_chunk.set_texture(head_shift)
                else:
                    snake_chunk.set_texture(forward_chunk_pos - snake_chunk.get_grid_position())

                forward_chunk_pos = snake_chunk.get_grid_position()

    def increase_size(self) -> None:
        # TODO: add logic to increase length of snake if edible is collided with
        body_chunk = Body(self.body_texture_map, self.cell_number, self.cell_size, self.chunks[1].get_grid_position())
        body_chunk.set_previous_grid_position(self.chunks[1].get_previous_grid_position())

        self.chunks.insert(1, body_chunk)
        self.chunks_group.add(body_chunk)
        self.collidable.add(body_chunk)

    def draw(self, surface: pygame.Surface) -> None:
        self.chunks_group.draw(surface)