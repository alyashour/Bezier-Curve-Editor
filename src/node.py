from __future__ import annotations

from engine import Point, colors

from .control_point import ControlPoint

class Node(Point):
    """Represents a node in a spline."""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color = colors.BLUE
        self._enabled = True

        # chain
        self._previous: Node | None = None
        self._next: Node | None = None
        
        # Node control points
        self.control_previous = ControlPoint(self)
        self.control_next = ControlPoint(self)
        ControlPoint.pair(self.control_previous, self.control_next) # pair them together

        # by default we'll have 1
        self.control_previous._enabled = True
        self.control_previous.x = 0
        self.control_previous.y = 50

    """
    Node Managed Properties.
    Google says these are very bad for performance so I should move to a better solution.
    Maybe moving the responsibility up to the spline or something.
    """
    @property
    def is_intermediate_node(self) -> bool:
        return bool(self.previous and self.next)

    # next node
    @property
    def next(self):
        return self._next
    
    @next.setter
    def next(self, value: Node):
        self._next = value

        self._check_control_point_count()

    # previous node
    @property
    def previous(self):
        return self._previous
    
    @previous.setter
    def previous(self, value: Node):
        self._previous = value

        self._check_control_point_count()

    @property
    def _control_1_abs(self):
        if self.control_previous._enabled:
            return self.control_previous + self
        
        return None
    
    @property
    def _control_2_abs(self):
        if self.control_next._enabled:
            return self.control_next + self
        
        return None

    # other methods
    def _check_control_point_count(self):
        # if we have a previous then we should have a control 1
        if self.previous:
            # if we don't then create one
            if not self.control_previous._enabled:
                self.control_previous._enabled = True
        # if we don't have a previous then we mustn't have a control_1
        else:
            self.control_previous._enabled = False

        # if we have a next then we should have a control 2
        if self.next:
            # if we don't then create one
            if not self.control_next._enabled:
                self.control_next._enabled = True
        else:
            self.control_next._enabled = False

    def get_control_points(self) -> tuple[Point]:
        """Gets the node's control points. All the control points have positions relative to the central node."""
        return tuple(c for c in (self.control_previous, self.control_next) if c is not None and c._enabled)
    
    def get_abs_control_points(self) -> tuple[Point]:
        """Gets the node's control points. Their positions are absolute."""
        return tuple(n + self for n in self.get_control_points())
    
    def unwrap_abs(self) -> tuple[Point]:
        """
        Returns all of the points in this node (main and control points) in order, in absolute coordinates.
        Note: original references are NOT maintained for control points.
        """
        return tuple(c for c in (self._control_1_abs, self, self._control_2_abs) if c is not None)
    
    def unwrap(self) -> tuple[Point]:
        """
        Returns all of the points in this node (main and control points) in order, in absolute coordinates.
        References are maintained.
        """
        return tuple(c for c in (self.control_previous, self, self.control_next) if c._enabled)


    