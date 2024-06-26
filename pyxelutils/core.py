import weakref
import copy
import threading

from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict


class Types(Enum):
    BASE = 0
    COLLIDER = 1
    TRANSFORM = 2
    HERO = 3


class OrderedSet:
    def __init__(self, weak=True):
        if weak:
            self._data = weakref.WeakKeyDictionary()
        else:
            self._data = dict()

    def add(self, item):
        self._data[item] = None

    def remove(self, item):
        del self._data[item]

    def pop_item(self, item):
        if item in self._data:
            k = item
            self._data.pop(item)
            return k

    def pop(self):
        return self._data.pop(0)

    def clear(self):
        self._data.clear()

    def __iter__(self):
        return iter(self._data.keys())

    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"OrderedSet({list(self._data.keys())})"

    def __getitem__(self, index):
        return list(self._data.keys())[index]


class SpatialColliderGrid:
    def __init__(self, cell_size=20):
        self.cell_size = cell_size
        self.grid = defaultdict(OrderedSet)

    def _get_cell_coords(self, x, y):
        return x // self.cell_size, y // self.cell_size

    def update_collider(self, collider):
        self.remove_colliders(collider)

        min_cell_x, min_cell_y = self._get_cell_coords(collider.bbox[0], collider.bbox[1])
        max_cell_x, max_cell_y = self._get_cell_coords(collider.bbox[0] + collider.w, collider.bbox[1] + collider.h)

        for cell_x in range(min_cell_x, max_cell_x + 1):
            for cell_y in range(min_cell_y, max_cell_y + 1):
                self.grid[(cell_x, cell_y)].add(collider)

    def remove_colliders(self, collider):
        cell_coords = self._get_cell_coords(collider.bbox[0], collider.bbox[1])
        if collider in self.grid[cell_coords]:
            self.grid[cell_coords].remove(collider)

    def get_potential_colliders(self, x, y):
        cell_coords = self._get_cell_coords(x, y)
        return self.grid[cell_coords]


class Layer:
    FOREGROUND = 2
    MIDDLEGROUND = 1
    BACKGROUND = 0

    def __init__(self):
        self.foreground = OrderedSet()  # 2
        self.middleground = OrderedSet()  # 1
        self.background = OrderedSet()  # 0
        self.all = OrderedSet(weak=False)

    def add(self, obj, layer=1):
        def _add(obj, layer):
            if layer == 0:
                self.background.add(obj)
            elif layer == 1:
                self.middleground.add(obj)
            elif layer == 2:
                self.foreground.add(obj)
            else:
                raise ValueError("Layer index doesn't exist")
            self.all.add(obj)
            if obj.children:
                for c in obj.children:
                    _add(c, layer)
        _add(obj, layer)

    def remove(self, obj, layer=1):
        def _remove(obj, layer):
            if layer == 0:
                self.background.remove(obj)
            elif layer == 1:
                self.middleground.remove(obj)
            elif layer == 2:
                self.foreground.remove(obj)
            else:
                raise ValueError("Layer index doesn't exist")
            self.all.remove(obj)
            if obj.children:
                for c in obj.children:
                    _remove(c, layer)
        _remove(obj, layer)

    def change_layer(self, obj, layer):
        obj_ref = self.foreground.pop_item(obj) or self.middleground.pop_item(obj) or self.background.pop_item(obj) or obj
        self.add(obj_ref, layer)
        for o in obj.children:
            obj_ref = self.foreground.pop_item(o) or self.middleground.pop_item(o) or self.background.pop_item(o) or o
            self.add(obj_ref, layer)


class BaseGameObject(ABC):
    TYPE = Types.BASE

    def __del__(self):
        print(f"{self} destroyed")

    def __repr__(self):
        original_repr = super().__repr__()
        return f"{original_repr[:-1]}, {self.name}>"

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        # self.__init__(*args, **kwargs)
        cls.register_instance(self)
        return self

    def __init_subclass__(cls, *args, **kwargs):
        cls._base_init(cls, *args, **kwargs)
        cls.game = BaseGame

    def _base_init(cls, name='baseName', user_update=None, user_draw=None, x=0, y=0):
        cls.name = name
        cls.user_update = user_update
        cls.user_draw = user_draw
        cls._active = True
        cls._parent = None
        cls.children = None
        cls._x = x
        cls._x_offset = 0
        cls._y = y
        cls._y_offset = 0
        cls.instance_at_end = False
        cls.inherit_transform = True

    @property
    def x(self):
        if self.parent and self.inherit_transform:
            return self.parent.x + self._x
        else:
            return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        if self.parent and self.inherit_transform:
            return self.parent.y + self._y
        else:
            return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def world_position(self):
        return self.x, self.y

    @property
    def local_position(self):
        return self._x, self._y

    @property
    def parent(self):
        if self._parent:
            return self._parent()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @property
    def id(cls):
        return id(cls)

    def register_instance(self):
        if self.instance_at_end:
            BaseGame.instance.run_at_end.add((BaseGame.register, self))
        else:
            BaseGame.register(self)

    def activate(self, value):
        self.active = value

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if self.children:
            for child in self.children:
                child.active = value
        self._active = value

    def parent_to(self, parent):
        self._parent = weakref.ref(parent)
        if parent.children is None:
            parent.children = OrderedSet()
        parent.children.add(self)


class Level:
    def __repr__(self):
        original_repr = super().__repr__()
        return f"{original_repr[:-1]}, {self.name}>"

    def __init__(self, name):
        self.register = Layer()
        self.name = name

        self._last_name = 'rootLevel'

    def __enter__(self):
        self._last_name = BaseGame.level_manager.active_level.name
        BaseGame.level_manager.active_level = BaseGame.level_manager.levels[self.name]

    def __exit__(self, exc_type, exc_val, exc_tb):
        BaseGame.level_manager.active_level = BaseGame.level_manager.levels[self._last_name]


class LevelManager:
    levels = {'rootLevel': Level('rootLevel')}
    _active_level = levels['rootLevel']

    @staticmethod
    def new_level(name: str):
        lvl = Level(name)
        LevelManager.levels[name] = lvl
        return lvl

    @property
    def active_level(self):
        return LevelManager._active_level

    @active_level.setter
    def active_level(self, lvl):
        if lvl.name in LevelManager.levels:
            LevelManager._active_level = lvl
        else:
            raise TypeError(f"Level {lvl} doesn't exist in LevelManager")

    def next(self):
        index = list(self.levels.keys()).index(self.active_level.name) + 1
        if len(self.levels) > index:
            name = list(self.levels.keys())[index]
            self.active_level = self.levels[name]
            return True
        else:
            return False

    def previous(self):
        index = list(self.levels.keys()).index(self.active_level.name) - 1
        if len(self.levels) > index >= 0:
            name = list(self.levels.keys())[index]
            self.active_level = self.levels[name]
            return True
        else:
            return False

    def add_instance_object(self, o):
        BaseGame.instance.run_at_end.add((self.active_level.register.add, o))

    def remove_instance_object(self, o):
        BaseGame.instance.run_at_end.add((self.active_level.register.add, o))

    def add_instance_objects_from_level(self, lvl):
        if isinstance(lvl, str):
            lvl = self.levels[lvl]
        for o in lvl.register.all:
            self.active_level.register.add(o)


class RunAtEnd:
    waiting_queue = OrderedSet(weak=False)
    queue = OrderedSet(weak=False)

    def add(self, value):
        self.queue.add(value)
        # if value not in self.queue:
        #     self.waiting_queue.add(value)

    def remove(self, value):
        self.queue.remove(value)
        # self.waiting_queue.remove(value)

    def turn_over(self):
        self.queue.clear()
        for o in self.waiting_queue:
            self.queue.add(o)
        self.waiting_queue.clear()

    def call(self):
        for fn, args in self.queue:
            print(f"call {fn}, {args}")
            if args is None:
                fn()
            else:
                fn(args)
        self.queue.clear()


class BaseGame:
    instance = None
    level_manager = LevelManager()
    colliders = OrderedSet()
    heroes = OrderedSet()
    _last_copy = None

    def __init_subclass__(cls, *args, **kwargs):
        cls._base_init(cls, *args, **kwargs)

    def _base_init(cls, pyxel, w, h, name='pyxelGame', fps=30, cls_color=0):
        cls.pyxel = pyxel
        cls.w = w
        cls.h = h
        cls.name = name
        cls.fps = fps
        cls.cls_color = cls_color
        cls.run_at_end = RunAtEnd()
        BaseGame.instance = cls

    @staticmethod
    def get_last_copy():
        last = BaseGame._last_copy
        BaseGame._last_copy = None
        return last

    @staticmethod
    def register(obj: BaseGameObject):
        BaseGame.level_manager.active_level.register.add(obj)
        if obj.TYPE == Types.COLLIDER:
            BaseGame.colliders.add(obj)
        if obj.TYPE == Types.HERO:
            BaseGame.heroes.add(obj)

    def init_game(self):
        self.pyxel.init(self.w, self.h, self.name, fps=self.fps)

    def run_game(self):
        self.pyxel.run(self.update, self.draw)

    @staticmethod
    def _update_single(obj):
        obj.update()
        if obj.user_update:
            obj.user_update(obj)

    def update(self):
        for o in BaseGame.level_manager.active_level.register.all:
            if o.active:
                self._update_colliders(o)
                self._update_single(o)
        self.run_at_end.call()

    @staticmethod
    def _update_colliders(obj):
        if obj.TYPE == Types.COLLIDER:
            # TODO : Fix Collider Grid
            for collider in BaseGame.colliders:
                if collider is obj:
                    continue
                if collider.has_overlapping(obj):
                    collider.overlap.add(obj)

    @staticmethod
    def _draw_single(obj):
        if obj.active:
            obj.draw()
            if obj.user_draw:
                obj.user_draw(obj)

    def draw(self):
        self.pyxel.cls(self.cls_color)
        for o in BaseGame.level_manager.active_level.register.background:
            self._draw_single(o)
        for o in BaseGame.level_manager.active_level.register.middleground:
            self._draw_single(o)
        for o in BaseGame.level_manager.active_level.register.foreground:
            self._draw_single(o)

    @staticmethod
    def _destroy(obj):
        def rec_destroy(obj):
            # parse level
            for level in BaseGame.level_manager.levels.values():
                if obj in level.register.all:
                    level.register.all.remove(obj)
                if obj in level.register.foreground:
                    level.register.foreground.remove(obj)
                if obj in level.register.middleground:
                    level.register.middleground.remove(obj)
                if obj in level.register.background:
                    level.register.background.remove(obj)
            # parse colliders
            if obj in BaseGame.colliders:
                BaseGame.colliders.remove(obj)
            # heroes
            if obj in BaseGame.heroes:
                BaseGame.heroes.remove(obj)
            # parse children
            if obj.children:
                for child in obj.children:
                    rec_destroy(child)
            del obj
        rec_destroy(obj)

    @staticmethod
    def destroy(obj):
        obj.active = False
        BaseGame.instance.run_at_end.add((BaseGame.instance._destroy, obj))

    @staticmethod
    def _copy(obj):
        obj2 = copy.deepcopy(obj)
        BaseGame._last_copy = obj2

    @staticmethod
    def copy(obj):
        BaseGame.instance.run_at_end.add((BaseGame._copy, obj))

    @staticmethod
    def run_at_end_with_delay(arg, delay=10):
        def _run_with_delay(arg):
            BaseGame.instance.run_at_end.add(arg)
        t = threading.Timer(delay, _run_with_delay, args=(arg,))
        t.start()
