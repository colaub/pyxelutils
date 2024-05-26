from pathlib import Path

from pyxelutils.pyxelutils import color, core, sprite, controllers, collider
import pyxel

from sprite_anim import ActionWalk


class ColumnCollider(collider.Collider):
    def logic(self):
        if self.overlap:
            for obj in self.overlap:
                overlap_left = obj.bbox[2] - self.bbox[0]
                overlap_right = self.bbox[2] - obj.bbox[0]
                overlap_top = obj.bbox[3]- self.bbox[1]
                overlap_bottom = self.bbox[3] - obj.bbox[1]

                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                if min_overlap == overlap_left:
                    obj.parent.x = self.bbox[0] - obj.w - obj.x  # push out obj on the left
                elif min_overlap == overlap_right:
                    obj.parent.x = self.bbox[2] - obj.x  # push out obj on the right
                elif min_overlap == overlap_top:
                    obj.parent.y = self.bbox[1] - obj.h - obj.y  # push out obj on the top
                elif min_overlap == overlap_bottom:
                    obj.parent.y = self.bbox[3] - obj.y  # push out obj on the bottom


class Dog:
    def __init__(self):
        self.sprite_side_walk = sprite.Sprite(0, 0, 0, 0, 0, 64, 32,
                                              [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)],
                                              5, trsp_col=9)

        self.sprite_up_walk = sprite.Sprite(0, 0, 0, 0, 0, 32, 32,
                                            [(0, 2), (1, 2), (2, 2), (0, 3), (1, 3)],
                                            5, trsp_col=9)

        self.sprite_down_walk = sprite.Sprite(0, 0, 0, 0, 0, 32, 32,
                                              [(3, 2), (4, 2), (5, 2), (3, 3), (4, 3), (5, 3)],
                                              5, trsp_col=9)

        self.ctrl = controllers.DirectionalKeysCtrl()
        self.action = ActionWalk(180, 10, 'walk', self.ctrl)
        self.action.add_sprite('side_walk', self.sprite_side_walk)
        self.action.add_sprite('up_walk', self.sprite_up_walk, offset_x=15)
        self.action.add_sprite('down_walk', self.sprite_down_walk, offset_x=15)



class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        color.add_palette(f'{Path(__file__).parent}/resources/palette_set.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')
        pyxel.images[1].load(0, 0, f'{Path(__file__).parent}/resources/set.png')

        dog = Dog()
        dog.action.change_layer(core.Layer.MIDDLEGROUND)

        column = sprite.Sprite(0, 0, 1, 0, 0, 32, 85,
                                              [(0, 0)],
                                              5, trsp_col=9)

        core.BaseGame.level_manager.active_level.register.change_layer(column, core.Layer.BACKGROUND)

        bag = sprite.Sprite(64, 85-32, 1, 32, 0, 32, 32,
                                              [(1, 0)],
                                              5, trsp_col=9)
        core.BaseGame.level_manager.active_level.register.change_layer(bag, core.Layer.FOREGROUND)

        column2_p1 = sprite.Sprite(64*2, 65, 1, 0, 32, 32, 32,
                                              [(0, 2)],
                                              5, trsp_col=9)

        core.BaseGame.level_manager.active_level.register.change_layer(column2_p1, core.Layer.BACKGROUND)

        column2_p2 = sprite.Sprite(64*2, 0, 1, 0, 0, 32, 65,
                                              [(0, 0)],
                                              5, trsp_col=9)

        core.BaseGame.level_manager.active_level.register.change_layer(column2_p2, core.Layer.FOREGROUND)

        bag2 = sprite.Sprite(64*3, 85-32, 1, 32, 0, 32, 32,
                                              [(1, 0)],
                                              5, trsp_col=9)

        core.BaseGame.level_manager.active_level.register.change_layer(bag2, core.Layer.FOREGROUND)

        coll_dog = collider.Collider(10, 25, dog.action.current.w - 20, 10, relative=True, debug=True)
        coll_dog.parent_to(dog.action)
        coll_dog.name = 'colliderDog'

        coll_column = collider.PhysicalCollider(0, 0, column2_p1.w, 25, debug=True)
        coll_column.parent_to(column2_p1)
        coll_column.name = 'colliderColumn'


Game().run_game()
