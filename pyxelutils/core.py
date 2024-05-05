from abc import ABC, abstractmethod


class OrderedSet:
    def __init__(self):
        self._data = dict()

    def add(self, item):
        self._data[item] = None

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


class BaseGameObject(ABC):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        cls.register_instance(self)
        return self

    def __init_subclass__(cls, *args, **kwargs):
        cls._base_init(cls, *args, **kwargs)
        cls.game = BaseGame

    def _base_init(cls, name='baseName', user_update=None, user_draw=None):
        cls.name = name
        cls.user_update = user_update
        cls.user_draw = user_draw

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @property
    def id(cls):
        return id(cls)

    @staticmethod
    def register_instance(self):
        BaseGame.register(self)



class Level:
    def __repr__(self):
        original_repr = super().__repr__()
        return f"{original_repr[:-1]}, {self.name})"

    def __init__(self, name):
        self.register = OrderedSet()
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


class BaseGame:
    instance = None
    level_manager = LevelManager()

    def __init_subclass__(cls, *args, **kwargs):
        cls._base_init(cls, *args, **kwargs)

    def _base_init(cls, pyxel, w, h, name='pyxelGame', fps=30, cls_color=0):
        cls.pyxel = pyxel
        cls.w = w
        cls.h = h
        cls.name = name
        cls.fps = fps
        cls.cls_color = cls_color
        BaseGame.instance = cls

    @staticmethod
    def register(obj: BaseGameObject):
        BaseGame.level_manager.active_level.register.add(obj)

    def init_game(self):
        self.pyxel.init(self.w, self.h, self.name, fps=self.fps)

    def run_game(self):
        self.pyxel.run(self.update, self.draw)

    def update(self):
        for o in BaseGame.level_manager.active_level.register:
            o.update()
            if o.user_update:
                o.user_update(o)

    def draw(self):
        self.pyxel.cls(self.cls_color)
        for o in BaseGame.level_manager.active_level.register:
            o.draw()
            if o.user_draw:
                o.user_draw(o)


