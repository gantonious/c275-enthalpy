class Entity:
    """
    projectiles, players, bosses, (enemies)
    """
    def __init__(self, ID, health, width, height, x, y, hitbox, damage, color):
        self._ID = ID
        self._health = health
        self._width = width
        self._height = height
        self._x = x
        self._y = y
        self._hitbox_size = hitbox
        self._damage = damage
        self._color = color

    def update_health(self, damage):
        self._health += damage

    def get_health(self):
        return self._health

    def get_ID(self):
        return self._ID

    def get_coords(self):
        return (self._x + (self._width - self._hitbox_size)/2, \
            self._y + (self._height - self._hitbox_size)/2, \
            self._hitbox_size, self._hitbox_size)

    def collide(self, target):
        if target.get_ID() == self._ID:
            return 0
        coords = target.get_coords()
        if (self._x + self._width > coords[0] and \
            self._x < coords[0] + coords[2] and \
            self._y + self._height > coords[1] and \
            self._y < coords[1] + coords[3]):
            self._state = 0
            target.update_health(-1*self._damage)
            return 1
        return 0