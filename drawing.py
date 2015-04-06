"""
A whole bunch of drawing functions
"""
import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)

def draw_entity(screen, entity):
    pygame.draw.rect(screen, entity.color, entity.get_position(), 2)

def draw_hit_box(screen, entity):
    pygame.draw.rect(screen, entity.color, entity.get_coords(), 2)