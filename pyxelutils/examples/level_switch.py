from pyxelutils.pyxelutils import text, core
import pyxel


class SwitchLevelPushBtn(core.BaseGameObject):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            print("switch level")
            core.BaseGame.level_manager.next() or core.BaseGame.level_manager.previous()

    def draw(self):
        pass


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224):

    def __init__(self):
        # must be called at the top
        self.init_game()

        self.pp = SwitchLevelPushBtn()
        txt = f"{self.level_manager.active_level}".split("at")[1]
        self.txt = text.Simple((self.w / 2 - len(txt) * 2), self.h / 2, f"({txt}")
        self.txt = text.Simple((self.w / 2 - len(txt) * 2), (self.h / 2) + 15, f'item one')

        # create a new level, every object created in with block will be added to this level register
        with self.level_manager.new_level('level1'):
            self.pp = SwitchLevelPushBtn()
            txt = f"{self.level_manager.active_level}".split("at")[1]
            self.txt = text.Simple((self.w / 2 - len(txt) * 2), self.h / 2, f"({txt}")
            self.txt = text.Simple((self.w / 2 - len(txt) * 2), (self.h / 2) + 15, f'item two')


        # must be called at the end or by the instance
        self.run_game()


Game()
