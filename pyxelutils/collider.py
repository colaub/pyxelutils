import pyxel
from . import core


class Collider(core.BaseGameObject):
    TYPE = core.Types.COLLIDER

    def __init__(self, x, y, w, h, subtype=None, debug=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.debug = debug
        self.inside = core.OrderedSet()
        self.overlap = core.OrderedSet()
        self.subtype = subtype

        self.bbox = (self.x, self.y, self.x + self.w, self.y + self.h)

    def update(self):
        self.bbox = (self.x, self.y,
                     self.x + self.w,
                     self.y + self.h)
        if self.overlap and pyxel.frame_count > 0:
            for obj in self.overlap:
                if self.subtype:
                    if isinstance(obj.parent, self.subtype):
                        self.logic(obj)
                        core.BaseGame.instance.run_at_end.add((self.overlap.remove, obj))

    def logic(self, obj):
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
    def logic(self, obj):
        if self.overlap and pyxel.frame_count > 0:
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


class DestroyCollider(Collider):
    def logic(self, obj):
        core.BaseGame.instance.destroy(obj.parent)


class OutOfScreenCollider(Collider):
    def __init__(self, subtype=None):
        super().__init__(0, 0, core.BaseGame.instance.w, core.BaseGame.instance.h, subtype=subtype)
        self.was_overlapped = core.OrderedSet()

    def update(self):
        self.bbox = (self.x, self.y,
                     self.x + self.w,
                     self.y + self.h)
        if self.overlap and pyxel.frame_count > 0:
            for obj in self.overlap:
                if self.subtype and not isinstance(obj.parent, self.subtype):
                    continue
                self.was_overlapped.add(obj)
                for obj in self.was_overlapped:
                    if obj not in self.overlap:
                        self.logic(obj)


class DestroyOutOfScreenCollider(OutOfScreenCollider):
    def __init__(self, subtype=None):
        super().__init__(subtype=subtype)
        self.was_overlapped = core.OrderedSet()

    def logic(self, obj):
        core.BaseGame.instance.destroy(obj.parent)
