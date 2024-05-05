from pyxelutils.pyxelutils import text, core
import pyxel


class Game(core.BaseGame, pyxel=pyxel, w=256, h=224):

    def __init__(self):
        self.init_game()
        self.txt = text.InRect(10, 150, 237, 51,
                               "Un garbage collector est un mécanisme de gestion automatique de la mémoire qui "
                               "identifie et libère les blocs de mémoire inutilisés (garbage) afin de les réutiliser."
                               " Il permet d'éviter les fuites de mémoire en libérant automatiquement la mémoire "
                               "allouée aux objets qui ne sont plus référencés."
                               "allouée aux objets qui ne sont plus référencés."
                               "allouée aux objets qui ne sont plus référencés."
                               "allouée aux objets qui ne sont plus référencés."
                               "allouée aux objets qui ne sont plus référencés."
                               "allouée aux objets qui ne sont plus référencés."
                               , edit=False)
        def debug_txt(txt):
            """
            Add extra call at the end of original update()
            Exist also for draw()
            :param txt: the instance given as argument by the caller
            """
            if pyxel.frame_count > 50:
                txt.txt = "Make a Bug!"

        self.txt.user_update = debug_txt

        self.run_game()
Game()
