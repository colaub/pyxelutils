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

    def _base_init(cls, name='baseName'):
        cls.name = name

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
        BaseGame.register.add(self)


class BaseGame:
    register = OrderedSet()
    instance = None

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

    def init_game(self):
        self.pyxel.init(self.w, self.h, self.name, fps=self.fps)

    def run_game(self):
        self.pyxel.run(self.update, self.draw)

    def update(self):
        for o in BaseGame.register:
            o.update()

    def draw(self):
        self.pyxel.cls(self.cls_color)
        for o in BaseGame.register:
            o.draw()


