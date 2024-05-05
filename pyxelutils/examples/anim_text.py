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
        self.run_game()


Game()
