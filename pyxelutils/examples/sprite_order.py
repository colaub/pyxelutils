from pathlib import Path

import pyxel
from pyxelutils.pyxelutils import color, core, sprite, controllers, collider

from dog_actor import Dog


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        color.add_palette(f'{Path(__file__).parent}/resources/palette_set.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')
        pyxel.images[1].load(0, 0, f'{Path(__file__).parent}/resources/set.png')

        dog = Dog()
        dog.action.change_layer(core.Layer.FOREGROUND)

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
        column2_p1.name = 'colum2p1'
        core.BaseGame.level_manager.active_level.register.change_layer(column2_p1, core.Layer.BACKGROUND)

        column2_p2 = sprite.Sprite(64*2, 0, 1, 0, 0, 32, 65,
                                              [(0, 0)],
                                              5, trsp_col=9)
        column2_p1.name = 'colum2p2'
        core.BaseGame.level_manager.active_level.register.change_layer(column2_p2, core.Layer.FOREGROUND)

        bag2 = sprite.Sprite(64*3, 85-32, 1, 32, 0, 32, 32,
                                              [(1, 0)],
                                              5, trsp_col=9)

        core.BaseGame.level_manager.active_level.register.change_layer(bag2, core.Layer.FOREGROUND)


Game().run_game()
