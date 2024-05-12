import pyxel

from . import core
from . import mouse as mouse_utils



class DirectionalKeysCtrl(core.BaseGameObject):
    def __init__(self):
        self.direction = [0,0]

    def update(self):
        self.direction = [0, 0]
        if pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_LEFT):
            self.direction[0] = -1
            self.direction[1] = -1
        elif pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_RIGHT):
            self.direction[0] = 1
            self.direction[1] = -1
        elif pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_LEFT):
            self.direction[0] = -1
            self.direction[1] = 1
        elif pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_RIGHT):
            self.direction[0] = 1
            self.direction[1] = 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.direction[0] = -1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.direction[0] = 1
        elif pyxel.btn(pyxel.KEY_UP):
            self.direction[1] = -1
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direction[1] = 1
        elif pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_LEFT):
            self.direction[0] = -1
            self.direction[1] = -1

    def draw(self):
        pass


class MousePointToGround(core.BaseGameObject):
    def __init__(self, bbox_ground, mouse=None, offset_x=0, offset_y=0):
        self.mouse = mouse or mouse_utils.Mouse()
        self.bbox_ground = bbox_ground
        self.y_ground = self.bbox_ground[1]
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.pos = ()

    def update(self):
        if self.mouse.is_clicked:
            self.pos = (self.mouse.clicked_mouse_x + self.offset_x, self.y_ground + self.offset_y)

    def draw(self):
        pass
