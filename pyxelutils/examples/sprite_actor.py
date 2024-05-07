from pathlib import Path

from pyxelutils.pyxelutils import color, core, sprite
import pyxel


class ControllerDir(core.BaseGameObject):
    def __init__(self):
        self.dir = None

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.dir = pyxel.KEY_LEFT
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dir = pyxel.KEY_RIGHT
        else:
            self.dir = None

    def draw(self):
        pass


class TestSprite(core.BaseGameObject):

    def __init__(self):

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        self.frame_duration = 6
        self.flip_w = False
        self.flip_h = False

        self.sprite_w = 64
        self.sprite_h = 32

        self.transparent_color = 9

        self.sprite = sprite.Sprite(0, 0, 0, 0, 0, 256, 64, trsp_col=9)

        self.ctrl = ControllerDir()

        self.last_index = 0

    def update(self):
        pass

    def draw(self):
        pyxel.cls(1)
        # if self.ctrl.dir is not None:
        #     self.flip_w = True if self.ctrl.dir == pyxel.KEY_LEFT else False
        #     sprite_index = (pyxel.frame_count // 8) % 6
        #     self.last_index = sprite_index
        # else:
        #     sprite_index = self.last_index
        #
        # u = (sprite_index % 3) * 64
        # v = (sprite_index // 3) * 32
        #
        # pyxel.blt(50, 50, 0,
        #           u, v,
        #           -self.sprite_w if self.flip_w else self.sprite_w, -self.sprite_h if self.flip_h else self.sprite_h,
        #           self.transparent_color)


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224):
    def __init__(self):
        self.init_game()


        TestSprite()

        self.run_game()

Game()
