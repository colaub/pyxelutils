from pathlib import Path

import pyxel
from pyxelutils.pyxelutils import color, core, sprite, controllers, collider

from sprite_anim import ActionWalk


class Dog:
    def __init__(self):
        self.sprite_side_walk = sprite.Sprite(0, 0, 0, 0, 0, 64, 32,
                                              [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)],
                                              5, trsp_col=9)
        self.sprite_side_walk.name = 'side'
        self.sprite_up_walk = sprite.Sprite(0, 0, 0, 0, 0, 32, 32,
                                            [(0, 2), (1, 2), (2, 2), (0, 3), (1, 3)],
                                            5, trsp_col=9)

        self.sprite_down_walk = sprite.Sprite(0, 0, 0, 0, 0, 32, 32,
                                              [(3, 2), (4, 2), (5, 2), (3, 3), (4, 3), (5, 3)],
                                              5, trsp_col=9)
        self.sprite_down_walk.name = 'down'
        self.ctrl = controllers.DirectionalKeysCtrl()
        self.action = ActionWalk(180, 10, 'walk', self.ctrl)
        self.action.add_sprite('side_walk', self.sprite_side_walk)
        self.action.add_sprite('up_walk', self.sprite_up_walk, offset_x=15)
        self.action.add_sprite('down_walk', self.sprite_down_walk, offset_x=15)
        self.action.change_layer(core.Layer.MIDDLEGROUND)

class Column:
    def __init__(self):
        column = sprite.Sprite(0, 0, 1, 0, 0, 32, 85,
                                              [(0, 0)],
                                              5, trsp_col=9)
        core.BaseGame.level_manager.active_level.register.change_layer(column, core.Layer.BACKGROUND)
        self.bag = sprite.Sprite(64, 85-32, 1, 32, 0, 32, 32,
                                              [(1, 0)],
                                              5, trsp_col=9)
        core.BaseGame.level_manager.active_level.register.change_layer(self.bag, core.Layer.FOREGROUND)
        self.column2_p1 = sprite.Sprite(64*2, 65, 1, 0, 32, 32, 32,
                                              [(0, 2)],
                                              5, trsp_col=9)
        self.column2_p1.name = 'colum2p1'
        core.BaseGame.level_manager.active_level.register.change_layer(self.column2_p1, core.Layer.BACKGROUND)
        column2_p2 = sprite.Sprite(64*2, 0, 1, 0, 0, 32, 65,
                                              [(0, 0)],
                                              5, trsp_col=9)
        column2_p2.name = 'colum2p2'
        core.BaseGame.level_manager.active_level.register.change_layer(column2_p2, core.Layer.FOREGROUND)
        bag2 = sprite.Sprite(64*3, 85-32, 1, 32, 0, 32, 32,
                                              [(1, 0)],
                                              5, trsp_col=9)
        core.BaseGame.level_manager.active_level.register.change_layer(bag2, core.Layer.FOREGROUND)


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        color.add_palette(f'{Path(__file__).parent}/resources/palette_set.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')
        pyxel.images[1].load(0, 0, f'{Path(__file__).parent}/resources/set.png')

        dog = Dog()
        columns = Column()


        coll_dog = collider.Collider(10, 25, dog.action.current.w - 20, 10, relative=True, debug=True)
        coll_dog.parent_to(dog.action)
        coll_dog.name = 'colliderDog'

        coll_column = collider.PhysicalCollider(0, 0, columns.column2_p1.w, 25, debug=True)
        coll_column.parent_to(columns.column2_p1)
        coll_column.name = 'colliderColumn'

        coll_column = collider.DestroyCollider(0, 0, columns.bag.w, columns.bag.h, debug=True)
        coll_column.parent_to(columns.bag)
        coll_column.name = 'colliderBag'


Game().run_game()
