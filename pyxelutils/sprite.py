from abc import ABC, abstractmethod

import pyxel

from . import core


class BaseSprite(core.BaseGameObject):
    def __init__(self, x, y, img_bank: int, u, v, w, h, trsp_col: int = 0):
        self.x = x
        self.y = y
        self.img_bank = img_bank
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.trsp_col = trsp_col

        self.flip_w = False
        self.flip_h = False

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
            pyxel.blt(self.x, self.y, self.img_bank, self.u, self.v,
                      -self.w if self.flip_w else self.w, -self.h if self.flip_h else self.h,
                      self.trsp_col)


class Sprite(BaseSprite):
    def __init__(self, x, y, img_bank: int, u, v, w, h, sprite_range: list, frame_duration_per_sprite: int, trsp_col: int = 0):
        super().__init__(x, y, img_bank, u, v, w, h, trsp_col)

        def generator(lst: list):
            count = 0
            while True:
                yield lst[count]
                count += 1
                if count == len(lst):
                    count = 0

        self.sprite_range = sprite_range
        self.fdps = frame_duration_per_sprite

        self.index_generator = generator(self.sprite_range)
        self.last_animated_index = next(self.index_generator)

        self._stop = False

    def update(self):
        if not self._stop and pyxel.frame_count % self.fdps == 0:
            self.last_animated_index = next(self.index_generator)

        u = self.last_animated_index[0] * self.w
        v = self.last_animated_index[1] * self.h

        self.u = u
        self.v = v

    def reset(self):
        self.last_animated_index = self.sprite_range[0]

    def start(self):
        self._stop = False

    def stop(self):
        self._stop = True


class Action(core.BaseGameObject):
    def __init__(self, x: int, y: int, name: str, controller):
        self.x = x
        self.y = y
        self.name = name
        self.ctrl = controller
        self.sprites = dict()

        self._active = None

    def add_sprite(self, name: str, sprite: Sprite, offset_x: int = 0, offset_y: int = 0):
        sprite.stop()
        sprite.visible = False
        sprite.x = self.x + offset_x
        sprite.y = self.y + offset_y
        self.sprites[name] = sprite
        if len(self.sprites) == 1:
            self.active = name

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, name):
        self.invisible_all()
        self.sprites[name].visible = True
        self._active = self.sprites[name]

    def stop_all(self):
        for sprite in self.sprites.values():
            sprite.stop()

    def reset_all(self):
        for sprite in self.sprites.values():
            sprite.reset()

    def invisible_all(self):
        for sprite in self.sprites.values():
            sprite.visible = False

    def logic(self):
        raise NotImplementedError("'logic' must be implemented")

    def draw(self):
        pass

    def update(self):
        self.logic()
        for sprite in self.sprites.values():
            sprite.x = self.x
            sprite.y = self.y


