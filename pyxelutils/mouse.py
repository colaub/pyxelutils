import pyxel


def draw(col: int=0):
    pyxel.cls(col)
    pyxel.mouse(True)


def is_inside(bbox: tuple):
    if len(bbox) != 4:
        raise ValueError(f"Bbox must be a tuple length 4, given {bbox}")
    x_min, y_min, x_max, y_max = bbox
    return x_min < pyxel.mouse_x < x_max and y_min < pyxel.mouse_y < y_max


def drag(bbox: tuple):
    if len(bbox) != 4:
        raise ValueError(f"Bbox must be a tuple length 4, given {bbox}")


