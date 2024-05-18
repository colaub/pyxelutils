import pyxel


def load_palette(filename):
    """
    Load a palette to pyxel, replace the previous one
    :param filename: must a be palette file .hex
    """
    palette = []
    with open(filename, 'r') as f:
        for l in f.readlines():
            c = f"0x{l}"
            palette.append(int(c, 16))
    pyxel.colors.from_list(palette)


def add_palette(filename):
    """
    Add new palette to existing one

    :param filename: must a be palette file .hex
    """
    palette = pyxel.colors.to_list()
    with open(filename, 'r') as f:
        for l in f.readlines():
            c = f"0x{l}"
            palette.append(int(c, 16))
    pyxel.colors.from_list(palette)

