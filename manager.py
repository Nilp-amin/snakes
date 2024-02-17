#!/usr/bin/env python3
import pygame

from apple import Apple

from typing import List

class ScoreManager(object):
    FILL_COLOUR = (255, 255, 255)
    TEXT_COLOUR = (255, 255, 255)
    TEXT_SIZE = 128 
    def __init__(self, screen: pygame.display, cell_number: int, cell_size: int):
        # the screen to draw score updates upon
        self.screen = screen

        # text font
        # FIXME: update the font
        self.font = pygame.font.Font(None, ScoreManager.TEXT_SIZE)

        # apple texture
        # FIXME: make all the coordinates relative to a single value or something
        apple = Apple(cell_number, cell_size)
        apple.set_grid_position(pygame.Vector2(cell_number - 3, cell_number - 2))

        self.apple_group = pygame.sprite.GroupSingle(apple)

        # score box position 
        self.score_box = pygame.Rect(cell_size * (cell_number - 3),
                                     cell_size * (cell_number - 2), 
                                     2.5 * cell_size, 
                                     cell_size)

        self.cell_number = cell_number
        self.cell_size = cell_size

    def get_grid_positions(self) -> List[pygame.Vector2]:
        # FIXME: make this not hard coded
        return [pygame.Vector2(self.cell_number - 3, self.cell_number - 2),
                pygame.Vector2(self.cell_number - 2, self.cell_number - 2),
                pygame.Vector2(self.cell_number - 1, self.cell_number - 2)]

    def update(self, score: bool) -> None:
        pygame.draw.rect(self.screen, 
                         ScoreManager.FILL_COLOUR, 
                         self.score_box,
                         width=10,
                         border_radius=int(self.cell_size / 4))

        # create the score text
        text = self.font.render(f"x {score}", True, ScoreManager.TEXT_COLOUR)
        text_rect = text.get_rect(centerx=self.cell_size * (self.cell_number - 2) + self.cell_size / 2,
                                  centery=self.cell_size * (self.cell_number - 2) + self.cell_size / 2)

        self.apple_group.draw(self.screen)
        self.screen.blit(text, text_rect)
