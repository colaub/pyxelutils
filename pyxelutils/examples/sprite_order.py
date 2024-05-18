from pathlib import Path

from pyxelutils.pyxelutils import color, core, sprite, controllers, text
import pyxel

from sprite_anim import ActionWalk


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
        self.action = ActionWalk(50, 50, 'walk', self.ctrl)
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

        column = sprite.Sprite(64, 85-32, 1, 32, 0, 32, 32,
                                              [(1, 0)],
                                              5, trsp_col=9)

        core.BaseGame.level_manager.active_level.register.change_layer(column, core.Layer.FOREGROUND)

        column = sprite.Sprite(64*2, 0, 1, 0, 0, 32, 85,
                                              [(0, 0)],
                                              5, trsp_col=9)

        core.BaseGame.level_manager.active_level.register.change_layer(column, core.Layer.BACKGROUND)

        column = sprite.Sprite(64*3, 85-32, 1, 32, 0, 32, 32,
                                              [(1, 0)],
                                              5, trsp_col=9)

        core.BaseGame.level_manager.active_level.register.change_layer(column, core.Layer.FOREGROUND)


Game().run_game()
