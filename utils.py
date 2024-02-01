#!/usr/bin/env python3
import pygame

def clip(surface: pygame.surface, x: int, y: int, x_size: int, y_size: int) -> pygame.surface:
    """Used to get a section of an image.
    """
    handle_surface = surface.copy()
    clip_rect = pygame.Rect(x, y, x_size, y_size)
    handle_surface.set_clip(clip_rect)
    image = surface.subsurface(handle_surface.get_clip())

    return image.copy()