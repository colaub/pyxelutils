from pathlib import Path

import pyxel
from pyxelutils.pyxelutils import color, core, sprite, controllers, actor


class ActionWalk(sprite.Action):
    def __init__(self, x: int, y: int, name: str, controller, dog):
        super().__init__(x, y, name, controller)
        self.dog = dog
        self.name = 'dogAction'

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
        if self.ctrl.direction == [0, 0]:
            self.current.stop()
        else:
            self.dog.x += self.ctrl.direction[0] * self.dog.speed
            self.dog.y += self.ctrl.direction[1] * self.dog.speed


class Dog(actor.Actor):
    TYPE = core.Types.HERO

    def __init__(self):
        self.life = 5
        self.speed = 2
        self.max_speed = 8

        ctrl = controllers.DirectionalKeysCtrl()
        self.action = ActionWalk(self.x, self.y, 'dogWalk', ctrl, self)

        sprite_side_walk = sprite.Sprite(0, 0, 0, 0, 0, 64, 32,
                                         [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)],
                                         self.max_speed // self.speed or 1, trsp_col=9)
        sprite_up_walk = sprite.Sprite(0, 0, 0, 0, 0, 32, 32,
                                       [(0, 2), (1, 2), (2, 2), (0, 3), (1, 3)],
                                       self.max_speed // self.speed or 1, trsp_col=9)
        sprite_down_walk = sprite.Sprite(0, 0, 0, 0, 0, 32, 32,
                                         [(3, 2), (4, 2), (5, 2), (3, 3), (4, 3), (5, 3)],
                                         self.max_speed // self.speed or 1, trsp_col=9)
        self.action.add_sprite('side_walk', sprite_side_walk)
        self.action.add_sprite('up_walk', sprite_up_walk, offset_x=15)
        self.action.add_sprite('down_walk', sprite_down_walk, offset_x=15)

        self.action.parent_to(self)

        self.name = 'dog'

    def is_dead(self):
        if self.life <= 0:
            core.BaseGame.instance.destroy(self)
            print("IS DEAD")

    def logic(self):
        # self.x = self.action.x
        # self.y = self.action.y

        self.is_dead()



class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        dog = Dog()

        self.run_game()


if __name__ == '__main__':
    Game()
