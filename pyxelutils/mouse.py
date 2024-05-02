import pyxel


def draw(col: int=0):
    pyxel.cls(col)
    pyxel.mouse(True)


def is_inside(bbox: tuple):
    if len(bbox) != 4:
        raise ValueError(f"Bbox must be a tuple length 4, given {bbox}")
    x_min, y_min, x_max, y_max = bbox
    return x_min < pyxel.mouse_x < x_max and y_min < pyxel.mouse_y < y_max


class Drag:
    def __init__(self, bbox):
        self.bbox = bbox
        self.updated_bbox = self.bbox
        if len(self.bbox) != 4:
            raise ValueError(f"Bbox must be a tuple length 4, given {self.bbox}")

        self.is_dragging = False
        self.is_ready = False

    def update(self):
        x_min, y_min, x_max, y_max = self.bbox

        if is_inside(self.bbox) and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.is_dragging = True
            print(f"{pyxel.frame_count}: Debug drag : inside + button")
        elif self.is_dragging and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.is_dragging = True
            print(f"{pyxel.frame_count}: Debug drag : dragging + button")
        elif self.is_dragging and not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.is_dragging = False
            print(f"{pyxel.frame_count}: Debug drag : dragging + NO button")
        else:
            self.is_dragging = False

        if self.is_dragging:
            offset_x = pyxel.mouse_x - x_min
            offset_y = pyxel.mouse_y - y_min
            print(
                f"{pyxel.frame_count}: Debug drag : mouse_x {pyxel.mouse_x} mouse_y {pyxel.mouse_y} x_min {x_min} y_min {y_min} offset_x {offset_x}, offset_y {offset_y}")
            self.updated_bbox = (pyxel.mouse_x, pyxel.mouse_y, pyxel.mouse_x + x_max, pyxel.mouse_y + y_max)

        # if not self.is_dragging and self.is_ready:
        #     self.is_ready = False

def drag(bbox: tuple):
    if len(bbox) != 4:
        raise ValueError(f"Bbox must be a tuple length 4, given {bbox}")
    x_min, y_min, x_max, y_max = bbox
    offset_x = 0
    offset_y = 0
    updated_bbox = bbox
    if is_inside(bbox) and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
        offset_x = pyxel.mouse_x - x_min
        offset_y = pyxel.mouse_y - y_min
        print(f"{pyxel.frame_count}: Debug drag : mouse_x {pyxel.mouse_x} mouse_y {pyxel.mouse_y} x_min {x_min} y_min {y_min} offset_x {offset_x}, offset_y {offset_y}")
        updated_bbox = (pyxel.mouse_x, pyxel.mouse_y, pyxel.mouse_x + x_max, pyxel.mouse_y + y_max)
        return updated_bbox


