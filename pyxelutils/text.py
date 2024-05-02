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

        self.font_h = 7
        self.font_w = 3
        self.font_gap = 1
        self.bbox_font_h = self.font_h + self.font_gap
        self.bbox_font_w = self.font_w + self.font_gap

        self.border = 4

        self.real_rect_h = self.h - self.border
        self.real_rect_w = self.w - self.border

        self.max_lines = self.real_rect_h // self.bbox_font_h
        self.max_columns = self.real_rect_w // self.bbox_font_w

        self.txt = txt
        self.txt_chunk = list()

        self.edit_bbox_pos = (0, 0, 0, 0)
        self._edit_txt_pos = f"({self.x},{self.y})"
        self.mouse_drag_pos = mouse.Drag(self.edit_bbox_pos)

        self.edit_bbox_w = (0, 0, 0, 0)
        self._edit_txt_w = f"w = {self.w}"
        self.mouse_drag_w = mouse.Drag(self.edit_bbox_w)

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

        if self.edit:
            mouse.draw(0)
            self.edit_bbox_pos = (self.x, self.y - 12, self.x + (len(self._edit_txt_pos) * self.bbox_font_w),
                                  (self.y - 12) + self.bbox_font_h)

            self.mouse_drag_pos.bbox = self.edit_bbox_pos
            self.mouse_drag_pos.update()
            if self.mouse_drag_pos.is_dragging:
                self.x, self.y = self.mouse_drag_pos.updated_bbox[0], self.mouse_drag_pos.updated_bbox[1]
                self._edit_txt_pos = f"({self.x},{self.y})"

            self.edit_bbox_w = (self.x + (self.w + 2), self.y + self.h - 5, self.x + (self.w + 5) + (len(self._edit_txt_w) * self.bbox_font_w), self.y + self.h - 5 + self.bbox_font_h)
            self.mouse_drag_w.bbox = self.edit_bbox_w
            self.mouse_drag_w.update()
            if self.mouse_drag_w.is_dragging:
                self.w, self.h = self.mouse_drag_w.updated_bbox[0], self.mouse_drag_w.updated_bbox[1]
                self.real_rect_h = self.h - self.border
                self.real_rect_w = self.w - self.border
                self.max_lines = self.real_rect_h // self.bbox_font_h
                self.max_columns = self.real_rect_w // self.bbox_font_w
                self._edit_txt_w = f"({self.x},{self.y})"

    def draw(self):
        if self.edit:
            pyxel.text(self.edit_bbox_pos[0], self.edit_bbox_pos[1] + 2, self._edit_txt_pos, self.col)
            pyxel.text(self.x, self.y + (self.h + 5), f"h = {self.h}", self.col)
            pyxel.text(self.edit_bbox_w[0] + 3, self.edit_bbox_w[1], self._edit_txt_w, self.col)

        pyxel.rectb(self.x, self.y, self.w, self.h, self.col)
        i = 0
        for txt in self.txt_chunk:
            if i == 0:
                pyxel.text(self.x + self.border, self.y + self.border, txt, self.col)
            else:
                pyxel.text(self.x + self.border, self.y + self.border + (i * self.bbox_font_h), txt, self.col)
            i += 1
