import pyxel

from . import mouse, timer, core


class Simple(core.BaseGameObject):
    def __init__(self, x: int, y: int, txt: str, col: int = 7):
        self.x = x
        self.pos_x = x
        self.pos_y = y
        self.y = y
        self.txt = txt
        self.col = col
        self.font_h = 7
        self.font_w = 3

        self.center = False

    def update(self):
        if self.center:
            offset_x = len(self.txt) * self.font_w
            offset_y = self.font_w
            self.x = self.pos_x
            self.y = self.pos_y
            self.x = self.x - (offset_x // 2 + len(self.txt) // 2)
            self.y = self.y - (offset_y // 2)

    def draw(self):
        pyxel.text(self.x, self.y, self.txt, self.col)


class InRect(core.BaseGameObject):
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

        self.update_rect()

        self.finished = False

        if self.edit:
            # to have full text init Animated Text by height row of the window
            h_rows = core.BaseGame.instance.h // self.bbox_font_h
        else:
            h_rows = self.max_lines
        self.txt_animated = [Animated(0,0, '', col=self.col) for _ in range(h_rows)]

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
            if i < len(self.txt_animated):
                self.txt_animated[i].txt = o

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
            txt.x = self.x + self.border
            txt.y = self.y + self.border + (i * self.bbox_font_h)
            if i > 0:
                if not self.txt_animated[i-1].done:
                    txt.reset()
            i += 1
        if all(txt.done for txt in self.txt_animated):
            self.finished = True


class Animated(core.BaseGameObject):
    def __init__(self, x, y, txt, col=7, speed=50):
        self.x = x
        self.y = y
        self.col = col
        self.txt = txt
        self.anim_speed = speed or 10
        self.timer = timer.Timer()

        self.reset()

    def reset(self):
        self.done = False
        self.index_display_letter = 0
        self.frame_count = 0
        self.timer.start()

    def update(self):
        if self.timer.elapsed_time >= 2 / self.anim_speed:
            self.timer.stop()
            self.timer.start()
            self.index_display_letter += 1
            if self.index_display_letter >= len(self.txt):
                self.index_display_letter = len(self.txt)
                self.done = True
                self.timer.stop()

    def draw(self):
        chunk_txt = self.txt[:self.index_display_letter]
        pyxel.text(self.x, self.y, chunk_txt, self.col)

