
import pyxel

from . import mouse


def draw_txt_rect(x: int, y: int, w: int, h: int, txt: str, col: int=7, edit: bool=False):
    # check minimal value for w and h

    font_h = 7
    font_w = 3
    font_gap = 1
    bbox_font_h = font_h + font_gap
    bbox_font_w = font_w + font_gap

    border = 4

    real_rect_h = h - border
    real_rect_w = w - border

    max_lines = real_rect_h // bbox_font_h
    max_columns = real_rect_w // bbox_font_w

    if edit:
        txt_pos = f"{x} x {y}"
        bbox_pos = (x, y -10, x + (len(txt_pos) * bbox_font_w), (y - 10) + bbox_font_h)
        if mouse.is_inside(bbox_pos):
            print(f"{pyxel.frame_count}: Debug inside")

        mouse.draw(0)
        pyxel.text(bbox_pos[0], bbox_pos[1], txt_pos, col)

        pyxel.text(x, y + (h + 5), f"h = {h}", col)
        pyxel.text(x + (w + 5), y + h - 5, f"w = {w}", col)

    txt_len = len(txt)
    txt_chunk = []

    for i in range(0, txt_len, max_columns):
        id_space = txt.rfind(' ', 0, max_columns)
        if id_space == -1:
            id_space = max_columns
        if i == 0:
            tab = '  '
        else:
            tab = ''
        txt_chunk.append(tab + txt[:id_space])
        txt = txt[id_space+1:]
    txt_chunk.append(txt)

    pyxel.rectb(x, y, w, h, col)
    i = 0
    for txt in txt_chunk:
        if i == 0:
            pyxel.text(x + border, y + border, txt, col)
        else:
            pyxel.text(x + border, y + border + (i * bbox_font_h), txt, col)
        i += 1





