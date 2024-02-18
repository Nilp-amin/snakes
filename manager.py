#!/usr/bin/env python3
import os
import pygame

from apple import Apple

from typing import List

class ScoreManager(object):
    FILL_COLOUR = (175, 215, 90)
    TEXT_COLOUR = (255, 255, 255)
    TEXT_SIZE = 64 
    def __init__(self, screen: pygame.Surface, cell_number: int, cell_size: int):
        # the screen to draw score updates upon
        self.screen = screen

        # text font
        font_path = os.path.join(os.getcwd(), "fonts", "RobotoMono-Regular.ttf")
        self.font = pygame.font.Font(font_path, ScoreManager.TEXT_SIZE)

        self.cell_number = cell_number
        self.cell_size = cell_size

    def update(self, score: int, deaths: int) -> None:
        score_text = self.font.render(f"Score: {score}", True, ScoreManager.TEXT_COLOUR)
        death_text = self.font.render(f"Deaths: {deaths}", True, ScoreManager.TEXT_COLOUR)
        death_rect = death_text.get_rect()

        self.screen.fill(ScoreManager.FILL_COLOUR)
        self.screen.blit(score_text, (10, 5))
        self.screen.blit(death_text, (self.screen.get_size()[0] - death_rect.width - 10, 5))
