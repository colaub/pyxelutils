import pyxel
from . import core


class Sprite(core.BaseGameObject):
    def __init__(self, x, y, img_bank: int, u, v, w, h, trsp_col:0):
        self.x = x
        self.y = y
        self.img_bank = img_bank
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.trsp_col = trsp_col

        self._visible = True

    @property
    def visible(self):
        return  self._visible

    @visible.setter
    def visible(self, value):
        if not isinstance(value, bool):
            raise TypeError("Visible value must be bool")
        self._visible = value

    def update(self):
        pass

    def draw(self):
        if self.visible:
            pyxel.blt(self.x, self.y, self.img_bank, self.u, self.v, self.w, self.h, self.trsp_col)

