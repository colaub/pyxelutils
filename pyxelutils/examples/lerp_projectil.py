from pathlib import Path

import pyxel
from pyxelutils.pyxelutils import color, core, anim, collider, actor
import dog_actor


class Bullet(core.BaseGameObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_pos = (self.x, self.y)
        self.lp = None
        self.speed = 6
        cl = collider.Collider(-8, -8, 12,12, debug=False)
        cl.parent_to(self)

    def fire(self):
        self.lp = anim.Lerp(self, (self.x, self.y), self.target_pos, speed=self.speed)

    def draw(self):
        pyxel.circ(self.x, self.y, 8, 8)

    def update(self):
        pass


class SpawnBtn(core.BaseGameObject):
    def __init__(self, spawner):
        self.spawner = spawner

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.spawner.spawn()

    def draw(self):
        pass


class Spawn(core.BaseGameObject):
    def __init__(self, x, y, ammo, rate):
        self.x = x
        self.y = y
        self.ammo = ammo
        self.spawn_rate = rate

    def update(self):
        if self.ammo and pyxel.frame_count % self.spawn_rate == 0:
            bullet = Bullet(self.x, self.y)
            target_pos = (core.BaseGame.heroes[0].x, core.BaseGame.heroes[0].y)
            bullet.target_pos = target_pos
            bullet.fire()
            self.ammo -= 1

    def draw(self):
        pass


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        dog = dog_actor.Dog()
        spw = Spawn(256, 224, 10, 20)
        SpawnBtn(spw)

        collider.DestroyOutOfScreenCollider(subtype=Bullet)

        self.run_game()


if __name__ == '__main__':
    Game()
