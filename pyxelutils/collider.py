import pyxel
from . import core


class Collider(core.BaseGameObject):
    TYPE = core.Types.COLLIDER

    def __init__(self, x, y, w, h, relative=True, debug=False):
        self.bbox = (x, y, x+w, y+h)
        self.relative = relative
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.debug = debug
        self.inside = core.OrderedSet()
        self.overlap = core.OrderedSet()

    def update(self):
        core.BaseGame.collider_grid.update_collider(self)
        if self.relative and self.parent:
            self.bbox = (self.parent.x + self.x,
                         self.parent.y + self.y,
                         self.parent.x + self.x + self.w,
                         self.parent.y + self.y + self.h)
        else:
            self.bbox = (self.x, self.y, self.x + self.w, self.y + self.h)
        self.logic()

    def logic(self):
        pass

    def draw(self):
        if self.debug:
            pyxel.rectb(self.bbox[0], self.bbox[1], self.w, self.h, 5)

    def has_overlapping(self, obj):
        res = not (self.bbox[2] < obj.bbox[0] or
                    self.bbox[0] > obj.bbox[2] or
                    self.bbox[3] < obj.bbox[1] or
                    self.bbox[1] > obj.bbox[3])
        return res


class PhysicalCollider(Collider):
    def __init__(self, x, y, w, h, relative=True, debug=False, subtype=None):
        super().__init__(x, y, w, h, relative=relative, debug=debug)
        self.subtype = subtype

    def logic(self):
        if self.overlap:
            for obj in self.overlap:
                if self.subtype and not isinstance(obj, self.subtype):
                    continue
                overlap_left = abs(obj.bbox[2] - self.bbox[0])
                overlap_right = abs(self.bbox[2] - obj.bbox[0])
                overlap_top = abs(obj.bbox[3] - self.bbox[1])
                overlap_bottom = abs(self.bbox[3] - obj.bbox[1])

                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                if min_overlap == overlap_left:
                    obj.parent.x = self.bbox[0] - obj.w - obj.x  # push out obj on the left
                elif min_overlap == overlap_right:
                    obj.parent.x = self.bbox[2] - obj.x  # push out obj on the right
                elif min_overlap == overlap_top:
                    obj.parent.y = self.bbox[1] - obj.h - obj.y  # push out obj on the top
                elif min_overlap == overlap_bottom:
                    obj.parent.y = self.bbox[3] - obj.y  # push out obj on the bottom

