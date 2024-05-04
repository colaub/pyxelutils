import pyxel

from . import mouse


class InRect:
    def __init__(self, x: int, y: int, w: int, h: int, txt: str, col: int = 7, edit: bool = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
        self.edit = edit
        self.anim = True

        self.font_h = 7
        self.font_w = 3
        self.font_gap = 1
        self.bbox_font_h = self.font_h + self.font_gap
        self.bbox_font_w = self.font_w + self.font_gap

        self.border = 4

        self.txt = txt
        self.txt_chunk = list()
        self.txt_animated = [Animated(0,0, ''), Animated(0,0, ''), Animated(0,0, ''), Animated(0,0, '')]
        self.update_rect()

        if edit:
            self.edit_bbox_pos = (0, 0, 0, 0)
            self._edit_txt_pos = f"({self.x},{self.y})"
            self.mouse_drag_pos = mouse.Drag(self.edit_bbox_pos, mouse.Mouse())

            self.edit_bbox_w = (0, 0, 0, 0)
            self.mouse_drag_w = mouse.Drag(self.edit_bbox_w, mouse.Mouse())

        if self.anim:
            self.index_display_letter = 0
            self.anim_speed = 2
            self.frame_count = 0


    def update_rect(self):
        self.real_rect_h = self.h - self.border
        self.real_rect_w = self.w - self.border
        self.max_lines = self.real_rect_h // self.bbox_font_h
        self.max_columns = self.real_rect_w // self.bbox_font_w
        self._edit_txt_w = f"w = {self.w}"

    def update(self):
        txt_len = len(self.txt)
        self.txt_chunk = list()
        txt = self.txt

        for i in range(0, txt_len, self.max_columns):
            id_space = txt.rfind(' ', 0, self.max_columns)
            if id_space == -1:
                id_space = self.max_columns
            self.txt_chunk.append(txt[:id_space])
            txt = txt[id_space + 1:]
        self.txt_chunk.append(txt)

        for i, o in enumerate(self.txt_chunk):
            self.txt_animated[i].txt = o
            self.txt_animated[i].update()
            if i != 0:
                if self.txt_animated[i-1].done:
                    self.txt_animated[i].update()

        if self.edit:
            self.edit_bbox_pos = (self.x - 2.5, self.y - 2.5, self.x + 5, self.y + 5)
            self.mouse_drag_pos.bbox = self.edit_bbox_pos
            self.mouse_drag_pos.update()
            if self.mouse_drag_pos.is_dragging:
                self.x, self.y = pyxel.mouse_x, pyxel.mouse_y
                self._edit_txt_pos = f"({self.x},{self.y})"

            self.edit_bbox_w = (self.x + self.w - 2.5, self.y + self.h - 2.5, self.x + self.w + 4, self.y + self.h + 4)
            self.mouse_drag_w.bbox = self.edit_bbox_w
            self.mouse_drag_w.update()
            if self.mouse_drag_w.is_dragging:
                self.w, self.h = pyxel.mouse_x - self.x, pyxel.mouse_y - self.y
                self.update_rect()

    def draw(self):
        if self.edit:
            self.mouse_drag_w.mouse.draw()
            pyxel.text(self.x - 10, self.y - 10, self._edit_txt_pos, self.col)
            pyxel.rectb(self.edit_bbox_pos[0], self.edit_bbox_pos[1], 5, 5, self.col)

            pyxel.text(self.x + self.w + 5, self.y + self.h - 6, self._edit_txt_w, self.col)
            pyxel.rectb(self.edit_bbox_w[0], self.edit_bbox_w[1], 5, 5, self.col)

            pyxel.text(self.x, self.y + (self.h + 5), f"h = {self.h}", self.col)

        pyxel.rectb(self.x, self.y, self.w, self.h, self.col)
        i = 0
        for txt in self.txt_animated:
            if i == 0:
                txt.x = self.x + self.border
                txt.y = self.y + self.border
                txt.draw()
            else:
                if self.txt_animated[i-1].done:
                    txt.x = self.x + self.border
                    txt.y = self.y + self.border + (i * self.bbox_font_h)
                    txt.draw()
            i += 1


class Animated:
    def __init__(self, x, y, txt, col=7):
        self.x = x
        self.y = y
        self.col = col

        self.txt = txt
        self.frame_count = 0
        self.anim_speed = 2
        self.index_display_letter = 0

        self.done = False

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.anim_speed:
            self.frame_count = 0
            self.index_display_letter += 1
            if self.index_display_letter >= len(self.txt):
                self.index_display_letter = len(self.txt)
                self.done = True

    def draw(self):
        l = self.txt[:self.index_display_letter]
        pyxel.text(self.x, self.y, l, self.col)
