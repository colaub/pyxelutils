import pyxel
import time
from . import core


class Mouse(core.BaseGameObject):
    def __init__(self, col=0):
        self.click_time = 30
        self.drag_time = 500
        self.col = col
        self.start_time = time.time() * 1000
        self.pressed_time = 0
        self.is_clicked = False
        self.is_drag = False
        self.clicked_mouse_x = 0
        self.clicked_mouse_y = 0

    @staticmethod
    def is_inside(bbox):
        if len(bbox) != 4:
            raise ValueError(f"Bbox must be a tuple length 4, given {bbox}")
        x_min, y_min, x_max, y_max = bbox
        res = x_min < pyxel.mouse_x < x_max and y_min < pyxel.mouse_y < y_max
        return res

    @staticmethod
    def clicked_inside(bbox):
        if len(bbox) != 4:
            raise ValueError(f"Bbox must be a tuple length 4, given {bbox}")
        if Mouse.is_inside(bbox) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return True
        return False

    def update(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            current_time = time.time() * 1000
            self.pressed_time = current_time - self.start_time
        else:
            self.pressed_time = 0
            self.start_time = time.time() * 1000
        if self.pressed_time > self.click_time:
            self.is_clicked = True
            if self.pressed_time > self.drag_time and (self.clicked_mouse_x, self.clicked_mouse_y) != (pyxel.mouse_x, pyxel.mouse_y):
                self.is_drag = True
                self.is_clicked = False
        else:
            self.is_clicked = False
            self.is_drag = False

        if self.pressed_time > self.drag_time:
            self.is_clicked = False
        else:
            self.is_drag = False

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.is_clicked = True

        # must be at the end
        if self.is_clicked:
            self.clicked_mouse_x = pyxel.mouse_x
            self.clicked_mouse_y = pyxel.mouse_y

    def draw(self):
        pyxel.mouse(True)


class Drag(core.BaseGameObject):
    def __init__(self, bbox, mouse: Mouse):
        self.mouse = mouse
        self.bbox = bbox
        self.updated_bbox = self.bbox
        if len(self.bbox) != 4:
            raise ValueError(f"Bbox must be a tuple length 4, given {self.bbox}")
        self.is_dragging = False
        self.was_inside = False

    def update(self):
        self.mouse.update()
        if self.mouse.is_inside(self.bbox) and self.mouse.is_clicked:
            self.is_dragging = True
            self.was_inside = True
        elif self.was_inside and self.mouse.is_drag:
            self.is_dragging = True
        else:
            self.is_dragging = False
            self.was_inside = False

    def draw(self):
        pass
