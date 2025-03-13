from __future__ import annotations
from typing import overload
from math import sqrt

class Point:
    def __init__(self, x, y, color=None):
        self._x = x
        self._y = y
        self.color = color

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value

    @overload
    def set_position(self, position: Point | tuple[float, float]) -> None: ...
    
    @overload
    def set_position(self, x: float, y: float) -> None: ...

    def set_position(self, position_or_x: Point | tuple[float, float] | float, y: float = None) -> None:
        position = None
        # if first param is a point or a tuple
        if (
            isinstance(position_or_x, Point) or
            (isinstance(position_or_x, tuple) and len(position_or_x) == 2)
        ):
            position = position_or_x
        # if first param is a number and second param is also a number
        elif isinstance(position_or_x, (int, float)) and isinstance(y, (int, float)):
            position = position_or_x, y
        else:
            raise TypeError("Expected a Point, a tuple (x, y), or two numbers")
        
        self.x, self.y = position
    
    def distance_to(self, p):
        dx = self[0] - p[0]
        dy = self[1] - p[1]

        return sqrt(dx ** 2 + dy ** 2)

    def slope_between(self, p):
        dx = self[0] - p[0]
        dy = self[1] - p[1]

        return dy/dx
    
    def magnitude(self):
        return sqrt(self._x ** 2 + self._y ** 2)
    
    def norm(self):
        return self / self.magnitude
    
    def normalize(self):
        self._x /= self.magnitude
        self._y /= self.magnitude

    def __iter__(self):
        return iter((self._x, self._y))
    
    def __getitem__(self, index):
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        else:
            raise IndexError("Index must be 0 or 1")
    
    def __add__(self, other):
        return Point(self[0] + other[0], self[1] + other[1])
    
    def __sub__(self, other):
        if other is None:
            return self
        
        return Point(self[0] - other[0], self[1] - other[0])
    
    def __rsub__(self, other):
        return Point(other[0] - self[0], other[1] - self[1])
    
    def __div__(self, other):
        return Point(self._x / other, self._y / other)
    
    def __repr__(self):
        return f"Point({self._x}, {self._y})"
    
    def __neg__(self):
        return Point(-self._x, -self._y)