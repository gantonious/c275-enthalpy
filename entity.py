# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

class Entity:
    """
    projectiles, players, bosses, (enemies)
    """
    def __init__(self, ID, damage=5, color=BLACK):
        # stuff that needs to be set: health, size, location, hitbox
        self._ID = ID
        self._damage = damage
        self._color = color

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health

    def update_health(self, damage):
        self._health += damage

    @property
    def ID(self):
        return self._ID

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        
    @property
    def hitbox(self):
        return self._hitbox
    @hitbox.setter
    def hitbox(self, hitbox):
        self._hitbox = hitbox

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, color):
        self._color = color
    
    
    def get_location(self):
        return (self._x, self._y)

    def set_location(self, location):
        # pass a tuple (x, y)
        self._x = location[0]
        self._y = location[1]

    def get_coords(self):
        # returns hitbox area
        return (self._x + (self._width - self._hitbox)/2, \
            self._y + (self._height - self._hitbox)/2, \
            self._hitbox, self._hitbox)

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