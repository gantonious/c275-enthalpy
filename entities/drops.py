import entities
from entities.entity import Entity

class Drop(Entity):
    def __init__(self):
        super().__init__(ID)
        # set by loader: timeout, score/health/lives/whatever parameter

    def collide(self, target):
        if target.ID not in [0,1]:
            return 0
        coords = target.get_coords()
        if (self._x + self._width > coords[0] and \
            self._x < coords[0] + coords[2] and \
            self._y + self._height > coords[1] and \
            self._y < coords[1] + coords[3]):
            use(target)
            return True
        return False

    def use(self, entity):
        # override this to do something to entity when grabbed
