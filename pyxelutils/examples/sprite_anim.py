from pathlib import Path

import setuptools

from pyxelutils.pyxelutils import color, core, sprite
import pyxel


class ControllerDir(core.BaseGameObject):
    def __init__(self):
        self.direction = [0,0]

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction[0] = -1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.direction[0] = 1
        elif pyxel.btn(pyxel.KEY_UP):
            self.direction[1] = -1
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direction[1] = 1
        else:
            self.direction = [0,0]

    def draw(self):
        pass


class ActionWalkSide(sprite.Action):
    def logic(self):
        if self.ctrl.direction[0] < 0:
            self.active = 'side_walk'
            self.active.flip_w = True
            self.active.start()
        if self.ctrl.direction[0] > 0:
            self.active = 'side_walk'
            self.active.flip_w = False
            self.active.start()
        if self.ctrl.direction[1] < 0:
            self.active = 'up_walk'
            self.active.start()
        if self.ctrl.direction == [0,0]:
            self.active.stop()
        else:
            self.x += self.ctrl.direction[0]
            self.y += self.ctrl.direction[1]





class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        self.sprite_side_walk = sprite.Sprite(0, 0, 0, 0, 0, 64, 32,
                                              [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1)],
                                              5, trsp_col=9)

        self.sprite_up_walk = sprite.Sprite(0, 0, 0, 0, 0, 32, 32,
                                            [(0, 2), (1, 2), (2, 2), (0, 3), (1, 3)],
                                            5, trsp_col=9)

        self.ctrl = ControllerDir()
        # self.action = ActionWalkSide([self.sprite_side_walk], self.ctrl)
        self.action = ActionWalkSide(50, 50, 'walk', self.ctrl)
        self.action.add_sprite('side_walk', self.sprite_side_walk)
        self.action.add_sprite('up_walk', self.sprite_up_walk, offset_x=15)

        self.run_game()

Game()
