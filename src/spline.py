from engine import Point
from .node import Node

class Spline:
    """
    Represents a spline.
    Basically just a doubly linked list.
    """
    def __init__(self):
        self.start: Node | None = None
        self.end: Node | None = None

        self._length = 0
    
    def is_empty(self):
        return self._length == 0
    
    def push_front(self, node: Node):
        if self.start is None:
            self.start = self.end = node  # First node in the list
        else:
            node.next = self.start  # Link new node to current head
            self.start.previous = node  # Link current head to new node
            self.start = node  # Update head

        self._length += 1

    def push_back(self, node: Node):
        if self.end is None:
            self.start = self.end = node  # First node in the list
        else:
            node.previous = self.end  # Link new node to current tail
            self.end.next = node  # Link current tail to new node
            self.end = node  # Update tail
        
        self._length += 1

    def pop_front(self):
        if self.start is None:
            return None  # List is empty
        
        data = self.start
        if self.start == self.end:  # Only one node
            self.start = self.end = None
        else:
            self.start = self.start.next  # Move head forward
            self.start.previous = None  # Remove reference to old head

        self._length -= 1

        return data

    def pop_back(self):
        if self.end is None:
            return None  # List is empty
        
        data = self.end
        if self.start == self.end:  # Only one node
            self.start = self.end = None
        else:
            self.end = self.end.previous  # Move tail backward
            self.end.next = None  # Remove reference to old tail
        self._length -= 1

        return data

    def push_nearest(self, node: Node):
        """
        Pushes the node either to the start or the end depending on what's nearest.
        """
        # if the list is empty just push, it doesn't matter
        if self.is_empty() or self.start == self.end:
            self.push_back(node)
        # otherwise pick the closest option
        else:
            d_to_s = node.distance_to(self.start)
            d_to_e = node.distance_to(self.end)

            # if the start is closer
            if d_to_s < d_to_e:
                self.push_front(node)
            # if the end is closer
            elif d_to_e < d_to_s:
                self.push_back(node)
            # if they're the same
            else:
                self.push_back(node) # doesn't matter, just pick one
    
    def unwrap_nodes_abs(self) -> list[Point]:
        """
        Unwraps all the nodes & control points in the spline into a list of points.
        List is in order (i.e., nodes and control points are beside eachother).
        Coordinates are absolute but references are not maintained.
        I.e., useful for rendering.

        Returns:
            list[Point]: _description_
        """
        out = []
        for node in self:
            out += node.unwrap_abs()
        return out
    
    def unwrap_nodes(self) -> list[Point]:
        """
        Unwraps all the nodes in the spline into a list of points.
        Coordinates are still relative but references are maintained.
        List is in order (i.e., nodes and control points are beside eachother).
        I.e., use if references to the actual point objects are needed.

        Returns:
            list[Point]: _description_
        """
        out = []
        for node in self:
            out += node.unwrap()
        return out
    
    def print_forward(self):
        """Prints the list from head to tail."""
        node = self.start
        while node:
            print(node, end=" <-> ")
            node = node.next
        print("None")

    def print_backward(self):
        """Prints the list from tail to head"""
        node = self.end
        while node:
            print(node.data, end=" <-> ")
            node = node.prev
        print("None")

    def get_nodes(self) -> list[Node]:
        """Returns all the nodes in the spline"""
        return [node for node in self]
    
    def get_control_points_abs(self):
        """
        Returns all the control points in the spline in absolute coordinates.
        Useful for rendering.
        """
        out = []
        for node in self:
            out += node.get_abs_control_points()
        return out
    
    def __iter__(self):
        """An iterator over the spline"""
        current = self.start
        while current:
            yield current
            current = current.next
    
    def __len__(self):
        return self._length
