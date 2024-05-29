from pathlib import Path
import random

import pyxel
from pyxelutils.pyxelutils import color, core, anim, collider, actor
import dog_actor


class Bullet(core.BaseGameObject):
    def __init__(self, x, y):
        self.size = 8
        self.x = x
        self.y = y
        self.target_pos = (self.x, self.y)
        self.lp = None
        self.speed = 6
        cl = collider.Collider(-self.size, -self.size, self.size + 4,self.size + 4, debug=False)
        cl.parent_to(self)

    def fire(self):
        self.lp = anim.Lerp(self, (self.x, self.y), self.target_pos, speed=self.speed)
        self.lp.parent_to(self)

    def draw(self):
        pyxel.circ(self.x, self.y, self.size, 8)

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
        if core.BaseGame.heroes and self.ammo and pyxel.frame_count % self.spawn_rate == 0:
            bullet = Bullet(self.x, self.y)
            bullet.name = f'bullet{pyxel.frame_count}'
            bullet.size = random.randint(2, 9)
            bullet.speed = random.randint(4, 11)
            target_pos = (core.BaseGame.heroes[0].x, core.BaseGame.heroes[0].y)
            bullet.target_pos = target_pos
            bullet.fire()
            self.ammo -= 1

    def draw(self):
        pass


class DogCollider(collider.Collider):
    def logic(self, obj):
        self.parent.life -= 1
        core.BaseGame.instance.destroy(obj.parent)
        print("BIM ! life : ", self.parent.life)



class Game(core.BaseGame, pyxel=pyxel, w=256, h=224, cls_color=1):
    def __init__(self):
        self.init_game()

        color.load_palette(f'{Path(__file__).parent}/resources/palette.hex')
        pyxel.images[0].load(0, 0, f'{Path(__file__).parent}/resources/walk.png')

        dog = dog_actor.Dog()
        spw = Spawn(256, 224, 1000, 10)
        SpawnBtn(spw)

        collider.DestroyOutOfScreenCollider(subtype=Bullet)

        dcol = DogCollider(10, 5, 48, 32, debug=True, subtype=Bullet)
        dcol.parent_to(dog)
        dcol.name = 'dogCollider'

        self.run_game()


if __name__ == '__main__':
    Game()
