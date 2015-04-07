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

def draw_health_bar(screen, entity):
	health = (entity.health, entity.max_health)
	entity_dimensions = entity.get_position()

	width = entity_dimensions[2]*1.2
	height = 3
	x = entity_dimensions[0] - entity_dimensions[2]*0.1
	y = entity_dimensions[1] - height*2

	pygame.draw.rect(screen, entity.color, (x, y, width, height), 1)
	pygame.draw.rect(screen, entity.color, (x, y, max(0, health[0] * width / health[1]), height))

def draw_hit_box(screen, entity):
    pygame.draw.rect(screen, entity.color, entity.get_coords(), 2)