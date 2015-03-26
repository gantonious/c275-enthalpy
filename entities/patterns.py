def fade_in(enemy, screen, factor):
    if abs(enemy.x_speed) < 1:
        x_speed = 0
    if abs(enemy.y_speed) < 1:
        y_speed = 0
    return x_speed * factor, y_speed * factor

def border(enemy, screen, border_speed):
    screen_size = screen.get_size()

    if enemy.x < 0:
        enemy.x = 0
    if enemy.x + enemy.width > screen_size[0]:
        enemy.x = screen_size[0] - enemy.width
    if enemy.y < 0:
        enemy.y = 0
    if enemy.y + enemy.height > screen_size[1]:
        enemy.y = screen_size[1] - enemy.width

    if enemy.x == 0: # down
        if enemy.y + enemy.height < screen_size[1]:
            return 0, border_speed
        else:
            return border_speed, 0
    if enemy.y + enemy.height == screen_size[1]: # right
        if enemy.x + enemy.width < screen_size[0]:
            return border_speed, 0
        else:
            return 0, -border_speed
    if enemy.x + enemy.width == screen_size[0]: # up
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
    x_distance = min(enemy.x, screen_size[0] - enemy.x) # closest x-border
    y_distance = min(enemy.y, screen_size[1] - enemy.y) # closest y-border

    if x_distance <= y_distance:
        if enemy.x + enemy.width < screen_size[0] - enemy.x:
            return -abs(border_speed), 0
        else:
            return abs(border_speed), 0
    if y_distance < x_distance:
        if enemy.y + enemy.height < screen_size[1] - enemy.y:
            return 0, -abs(border_speed)
        else:
            return 0, abs(border_speed)
