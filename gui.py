import pygame

class GUI:
	"""
	Handles any drawing
	"""
	BLACK    = (   0,   0,   0)
	WHITE    = ( 255, 255, 255)
	RED      = ( 255,   0,   0)

	def __init__(self, width, height):
		self._screen = pygame.display.set_mode([width, height])
		self._width = width
		self._height = height
		self.level_num = None
		self.level_name = None

	def draw_rect(self, entity):
		pygame.draw.rect(self._screen, entity.color, entity.get_position(), 2)

	def draw_hit_box(self, entity):
		pygame.draw.rect(self._screen, entity.color, entity.get_coords(), 2)

	def refresh(self):
		pygame.display.flip()


