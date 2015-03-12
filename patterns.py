def fade_in(x_speed, y_speed, factor):
    print(x_speed, y_speed)
    if abs(x_speed) < 1:
        x_speed = 0
    if abs(y_speed) < 1:
        y_speed = 0
    return x_speed * factor, y_speed * factor