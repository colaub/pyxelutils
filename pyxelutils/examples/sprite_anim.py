from pathlib import Path

from pyxelutils.pyxelutils import color, core, sprite, controllers, text
import pyxel


class ActionWalkToClick(sprite.Action):
    def logic(self):
        if self.ctrl.pos:
            if self.x == self.ctrl.pos[0]:
                self.current.stop()
            else:
                if self.ctrl.pos[0] < self.x:
                    self.current.flip_w = True
                else:
                    self.current.flip_w = False
                self.current = 'side_walk'
                self.current.start()
                self.move_until(self.ctrl.pos[0], self.ctrl.pos[1])
        else:
            self.current.stop()


class ActionWalk(sprite.Action):
    def logic(self):
        if self.ctrl.direction[0] < 0:
            self.current = 'side_walk'
            self.current.flip_w = True
            self.current.start()
        if self.ctrl.direction[0] > 0:
            self.current = 'side_walk'
            self.current.flip_w = False
            self.current.start()
        if self.ctrl.direction[1] < 0:
            self.current = 'up_walk'
            self.current.start()
        if self.ctrl.direction[1] > 0:
            self.current = 'down_walk'
            self.current.start()
        if self.ctrl.direction == [0,0]:
            self.current.stop()
        else:
            self.x += self.ctrl.direction[0]
            self.y += self.ctrl.direction[1]


class SwitchLevelPushBtn(core.BaseGameObject):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            print("switch level")
            core.BaseGame.level_manager.next() or core.BaseGame.level_manager.previous()

    def draw(self):
        pass


class ActivePushBtn(core.BaseGameObject):
    def __init__(self, action):
        self.action = action

    def update(self):
        if pyxel.btnp(pyxel.KEY_A):
            self.action.active = not self.action.active

    def draw(self):
        pass


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

        self.sprite_down_walk = sprite.Sprite(0, 0, 0, 0, 0, 32, 32,
                                            [(3, 2), (4, 2), (5, 2), (3, 3), (4, 3), (5, 3)],
                                            5, trsp_col=9)

        self.ctrl = controllers.DirectionalKeysCtrl()
        self.action = ActionWalk(50, 50, 'walk', self.ctrl)
        self.action.add_sprite('side_walk', self.sprite_side_walk)
        self.action.add_sprite('up_walk', self.sprite_up_walk, offset_x=15)
        self.action.add_sprite('down_walk', self.sprite_down_walk, offset_x=15)

        self.txt = text.Simple(30, 200, "SPACE BAR to switch controller")

        self.pp = SwitchLevelPushBtn()
        self.ap = ActivePushBtn(self.action)

        with self.level_manager.new_level('cltr_click'):

            self.level_manager.add_instance_object(self.pp)
            self.level_manager.add_instance_object(self.txt)

            self.sprite_side_walk = sprite.Sprite(50, 50, 0, 0, 0, 64, 32,
                                                  [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)],
                                                  5, trsp_col=9)
            self.ctrl = controllers.MousePointToGround((50, 50, 150, 150), offset_x=-32)
            self.action = ActionWalkToClick(50, 50, 'walk', self.ctrl)
            self.action.add_sprite('side_walk', self.sprite_side_walk)

        self.run_game()


if __name__ == '__main__':
    Game()
