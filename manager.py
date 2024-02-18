#!/usr/bin/env python3
import pygame

from apple import Apple

from typing import List

class ScoreManager(object):
    FILL_COLOUR = (175, 215, 90)
    TEXT_COLOUR = (255, 255, 255)
    TEXT_SIZE = 100 
    def __init__(self, screen: pygame.Surface, cell_number: int, cell_size: int):
        # the screen to draw score updates upon
        self.screen = screen

        # text font
        # FIXME: update the font
        self.font = pygame.font.Font(None, ScoreManager.TEXT_SIZE)

        self.cell_number = cell_number
        self.cell_size = cell_size

    def update(self, score: bool) -> None:

        text = self.font.render(f"Score: {score}", True, ScoreManager.TEXT_COLOUR)

        self.screen.fill(ScoreManager.FILL_COLOUR)
        self.screen.blit(text, (10, 20))
