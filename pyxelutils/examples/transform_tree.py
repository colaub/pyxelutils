from pathlib import Path

import pyxel
from pyxelutils.pyxelutils import color, core, anim, collider, actor
import dog_actor


class Circle(core.BaseGameObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        print(self.name, 'world :', self.world_position, 'local :', self.local_position)

    def draw(self):
        pyxel.circ(self.x, self.y, 4, 5)


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        dog = dog_actor.Dog()

        c1 = Circle(x=10, y=45)
        c1.parent_to(dog)
        c1.name = 'c1'

        c2 = Circle(x=10, y=45)
        c2.parent_to(c1)
        c2.name = 'c2'

        c3 = Circle(x=10, y=45)
        c3.parent_to(c2)
        c3.name = 'c3'

        self.run_game()


if __name__ == '__main__':
    Game()
