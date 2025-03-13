from typing import override

import glfw
from OpenGL.GL import *

from engine import App

from .node import Node
from .spline import Spline

class Assignment3(App):
    def __init__(self, width, height, window_name):
        super().__init__(width, height, window_name, 4)
        self.tolerance = 2 # how many times the size of a point should the area that counts as a valid click be?
        self._dragging = False
        self._dragged_node = None

        # initialize the spline
        self.spline = Spline()

        # reset the app when the user presses e
        self.input_manager.register_callback("key_press", self.reset, key_filter=glfw.KEY_E)

        # register mouse move, press, and release callbacks
        self.input_manager.register_callback("left_click", self.on_left_click)
        self.input_manager.register_callback("left_release", self.on_left_release)
        self.input_manager.register_callback("mouse_move", self.on_mouse_move)
        
        # set the point size
        self.renderer.default_point_size = 15
        self.renderer.default_line_width = 5

    @override
    # override how the user can exit the window to both be on escape AND on q
    def should_close(self):
        return self.input_manager.is_key_down(glfw.KEY_ESCAPE, glfw.KEY_Q)

    def _is_on_node(self, x, y):
        for node in self.spline.unwrap_nodes():
            if node.distance_to((x, y)) < self.tolerance * self.renderer.default_point_size:
                return True, node
        return False, None

    def on_left_click(self, x, y):
        is_on_node, node = self._is_on_node(x, y)
        if is_on_node:
            self._dragging = True
            self._dragged_node = node
        else:
            n = Node(x, y)
            self.spline.push_nearest(n)

    def on_left_release(self, x, y):
        self._dragging = False
        self._dragged_node = None
    
    def on_mouse_move(self, x, y):
        if self._dragging and self._dragged_node:
            self._dragged_node.set_position((x, y))

    def reset(self, key, scancode, mods):
        self.spline = Spline() # reset the spline
    
    def _draw_spline(self):
        points = self.spline.unwrap_nodes_abs()
        for i in range(0, len(points) - 3, 3):  # Iterate through groups of 4 points
            self.renderer.draw_cubic_bezier(points[i:i+4])
    
    def _get_spline_handles(self):
        points = []
        for node in self.spline:
            if node.control_next._enabled:
                points += (node, node.control_next.get_absolute_position())
            if node.control_previous._enabled:
                points += (node, node.control_previous.get_absolute_position())
        return points

    def draw(self):
        # draw the nodes
        self.renderer.draw_points(self.spline.get_nodes())
        # draw the control points
        self.renderer.draw_points(self.spline.get_control_points_abs(), round=True)
        # draw the spline
        self._draw_spline()
        # draw the control point handles
        self.renderer.draw_dotted_lines(self._get_spline_handles(), color=(0, 0.8, 0.6), scale_factor=2)
        