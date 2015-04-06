import entities, pygame
from math import copysign

def straight(enemy, dimensions, dt, params):
    enemy.wait_to_shoot = False
    if enemy.x_speed is None:
        if enemy.on_screen(dimensions):
            enemy.is_on_screen = True
        else:
            enemy.is_on_screen = False

    # enemy both came on screen and then left (never to come back)
    if enemy.is_on_screen and not enemy.on_screen(screen):
        enemy.despawn()

    return int(params[0]), int(params[1])

def fade_in(enemy, dimensions, dt, params):
    enemy.wait_to_shoot = True
    factor = int(params[2])

    if enemy.x_speed is None:
        enemy.x_speed = int(params[0])
        enemy.y_speed = int(params[1])
        enemy.initial_x_direction = copysign(1, enemy.x_speed)
        enemy.initial_y_direction = copysign(1, enemy.y_speed)

    if copysign(1, enemy.x_speed) != enemy.initial_x_direction or abs(enemy.x_speed) < 1:
        enemy.x_speed = 0
    if copysign(1, enemy.y_speed) != enemy.initial_y_direction or abs(enemy.y_speed) < 1:
        enemy.y_speed = 0

    return 0 if enemy.x_speed == 0 else enemy.x_speed - (factor*dt), \
           0 if enemy.y_speed == 0 else enemy.y_speed - (factor*dt)
    
def sweep(enemy, dimensions, dt, params):
    enemy.wait_to_shoot = False
    speed = int(params[0])
    delay = int(params[1])

    if enemy.x_speed is None:
        x_speed = speed
        enemy.delay = 0
        enemy.next_direction = 1

    if enemy.delay > 0:
        enemy.delay -= 1
        return 0, 0

    if enemy.x < 0:
        enemy.x = dimensions[0]
        x_speed = 0
        enemy.delay = delay
        enemy.next_direction = 1
    elif enemy.x + enemy.width > dimensions[0] + dimensions[2]:
        enemy.x = dimensions[0] + dimensions[2] - enemy.width
        x_speed = dimensions[0]
        enemy.delay = delay
        enemy.next_direction = -1
    else:
        x_speed = speed*enemy.next_direction

    return x_speed, 0

def border(enemy, dimensions, dt, params):
    enemy.wait_to_shoot = False
    border_speed = int(params[0])

    if enemy.x < 0:
        enemy.x = dimensions[0]
    if enemy.x + enemy.width > dimensions[0] + dimensions[2]:
        enemy.x = dimensions[0] + dimensions[2]  - enemy.width
    if enemy.y < 0:
        enemy.y = dimensions[1]
    if enemy.y + enemy.height > dimensions[1] + dimensions[3]:
        enemy.y = dimensions[1] + dimensions[3] - enemy.height

    if enemy.x == 0: # down
        if enemy.y + enemy.height < dimensions[1] + dimensions[3]:
            return 0, border_speed
        else:
            return border_speed, 0
    if enemy.y + enemy.height == dimensions[1] + dimensions[3]: # right
        if enemy.x + enemy.width < dimensions[0] + dimensions[2]:
            return border_speed, 0
        else:
            return 0, -border_speed
    if enemy.x + enemy.width == dimensions[0] + dimensions[2]: # up
        if enemy.y > 0:
            return 0, -border_speed
        else:
            return -border_speed, 0
    if enemy.y == 0: # left
        if enemy.x > 0:
            return -border_speed, 0
        else:
            return 0, border_speed

    # not on an edge
    x_distance = min(enemy.x, dimensions[0] + dimensions[2] - enemy.x) # closest x-border
    y_distance = min(enemy.y, dimensions[1] + dimensions[3] - enemy.y) # closest y-border

    if x_distance <= y_distance:
        if enemy.x + enemy.width < dimensions[0] + dimensions[2] - enemy.x:
            return -abs(border_speed), 0
        else:
            return abs(border_speed), 0
    if y_distance < x_distance:
        if enemy.y + enemy.height < dimensions[1] + dimensions[3] - enemy.y:
            return 0, -abs(border_speed)
        else:
            return 0, abs(border_speed)

entities.pattern_types["Straight"] = straight
entities.pattern_types["Border"] = border
entities.pattern_types["Sweep"] = sweep
entities.pattern_types["FadeIn"] = fade_in