import pyxel
from . import core, sprite


class Actor(core.BaseGameObject):

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        cls._base_init(cls, *args, **kwargs)

    def _base_init(cls):
        super()._base_init(cls)
        cls.x = 0
        cls.y = 0

    def update(self):
        self.logic()

    def draw(self):
        pass

    def logic(self):
        pass

