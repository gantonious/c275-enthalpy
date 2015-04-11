import entities, pygame, random
from entities.entity import Entity

class Drop(Entity):
    def __init__(self, x, y):
        super().__init__(-1)
        self._x = x + random.randint(-20, 20)
        self._y = y + random.randint(-20, 20)
        self._hitbox = self._x
        self._used = False
        # set by loader: timeout, score/health/lives/whatever parameter

    @property
    def used(self):
        return self._used

    def collide(self, target):
        if target.ID == 100: # enemies
            return False
        coords = target.get_position()
        if (self._x + self._width > coords[0] and \
            self._x < coords[0] + coords[2] and \
            self._y + self._height > coords[1] and \
            self._y < coords[1] + coords[3]):
            self.use(target)
            return True
        return False

    def use(self):
        # override this to do something to entity when grabbed
        self._used = True
        pass

class ScoreDrop(Drop):
    def __init__(self, x, y, params):
        super().__init__(x, y)
        self._score = int(params[0])
        self.color = (255, 255, 0)

    def use(self, entity):
        super().use()
        entity.score += self._score
        self.despawn()

class ShotSizeDrop(Drop):
    def __init__(self, x, y, params):
        super().__init__(x, y)
        self._factor = params[0] # multiplication factor
        self._time = params[1] # how long powerup lasts
        self._target = None
        self.color = (0, 255, 255)

    def use(self, entity):
        if not entity.shotsize_active:
            entity.shotsize_active = True
            self._target = entity
            self._use_time = pygame.time.get_ticks()
            entity.proj_size *= self._factor
        self._used = True

    def update(self):
        if self._target:
            if pygame.time.get_ticks() - self._use_time >= 1000*self._time:
                self._target.proj_size /= self._factor
                self._target.shotsize_active = False
                self.despawn()

class InvulnDrop(Drop):
    def __init__(self, x, y, params):
        super().__init__(x, y)
        self._time = params[0]
        self._target = None
        self.color = (255, 0, 255)

    def use(self, entity):
        if not entity.invuln_active:
            entity.invuln_active = True
            self._target = entity
            self._use_time = pygame.time.get_ticks()
            self._old_hitbox = entity.hitbox
            entity.hitbox = 0
        self._used = True

    def update(self):
        if self._target:
            if pygame.time.get_ticks() - self._use_time >= 1000*self._time:
                self._target.hitbox = self._old_hitbox
                self._target.invuln_active = False
                self.despawn()

entities.drop_types["Score"] = ScoreDrop
entities.drop_types["ShotSize"] = ShotSizeDrop
entities.drop_types["Invuln"] = InvulnDrop