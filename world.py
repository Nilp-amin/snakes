#!/usr/bin/env python3
import sys
import pygame

from apple import Apple
from boundry import Boundry
from snake import Snake

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
        
        # the apple object
        apple = Apple(cell_number, cell_size)

        # stores objects which cause collision
        # TODO: add walls to stop snake from going out of the screen
        self.collidable = pygame.sprite.Group(apple) 

        # stores the objects which can be eaten 
        self.edible = pygame.sprite.GroupSingle(apple)

        # the snake object
        self.snake = Snake(self.collidable, cell_number, cell_size)

        # the boundry object
        self.boundry = Boundry(self.collidable, cell_number, cell_size) 

        # queues the moves to be done in order
        self.move_queue = deque([]) 

        # if the game is over
        self.game_over = False

    def add_move(self, key: int) -> None:
        if key in World.ALLOWED_MOVES:
            self.move_queue.append(key)

    def check_for_collisions(self) -> bool:
        colliding_sprites = pygame.sprite.spritecollide(self.snake.get_head(), self.collidable, False)
        ate = False
        if colliding_sprites:
            for colliding_sprite in colliding_sprites:
                if isinstance(colliding_sprite, type(self.edible.sprite)):
                    # FIXME: add the positions of the snake chunks
                    colliding_sprite.set_random_position(set(pygame.Vector2(0.0)))
                    ate = True
                else: # invalid collision detected
                    self.game_over = True
                    break

        return ate 

    def draw_background(self) -> None:
        # set background colour of world 
        self._screen.fill(World.BACKGROUND_COLOUR)

        # set alternating grass pattern
        for row in range(self.cell_number):
            for col in range(self.cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(row * self.cell_size, col * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self._screen, World.GRASS_COLOUR, grass_rect)

    def update(self, dt: float) -> None:
        # FIXME: this needs to be here so that when eating a food that causes
        # extension of snake to overlap itself it ends immediatly
        ate = self.check_for_collisions()

        if self.game_over:
            # FIXME: update this to not just simply exit the game
            sys.exit(1)

        key = None
        if self.move_queue:
            key = self.move_queue.popleft()

        self.snake.advance_snake(key, ate)

        self.draw_background()
        self.edible.draw(self._screen)
        self.snake.draw(self._screen)
