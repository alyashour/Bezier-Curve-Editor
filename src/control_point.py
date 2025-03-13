from __future__ import annotations
from typing import override, overload

from engine import Point

class ControlPoint(Point):
    """
    Control points are like Nodes except internally their position is relative to the parent node 
    and they have a reference to a parent node and a partner control point.

    Control points can only be moved once they're paired to another control point and a node
    and their position is guaranteed to be colinear with the parent node and paired control point
    no matter what.

    Args:
        Point (_type_): _description_
    """
    def __init__(self, parent):
        super().__init__(0, 0)
        self.parent = parent

        self._enabled = False
        self._pair: ControlPoint = None

    @staticmethod
    def pair(p1: ControlPoint, p2: ControlPoint):
        p1._pair = p2
        p2._pair = p1

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        if self._pair is None:
            raise Exception("Control point must be paired before moving.")
        
        self._x = value
        self._pair._x = -value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        if self._pair is None:
            raise Exception("Control point must be paired before moving.")
        
        self._y = value
        self._pair._y = -value

    @override
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
        
        self.x, self.y = position - self.parent

    @override
    def distance_to(self, p):
        return (self + self.parent).distance_to(p)
    
    def get_absolute_position(self):
        return self + self.parent
    