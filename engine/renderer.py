from typing import Iterable, Union

from OpenGL.GL import *

from . import colors
from .point import Point

PointType = Union[Point, set]
ColorType = set[float]

class Renderer:
    def __init__(self, clear_color=colors.WHITE):
        self.clear_color = clear_color
        self._default_point_size = 1
        self._default_line_width = 1

    @property
    def default_point_size(self):
        return self._default_point_size

    @default_point_size.setter
    def default_point_size(self, value: float):
        glPointSize(value)
        self._default_point_size = value

    @property
    def default_line_width(self) -> float:
        return self._default_line_width
    
    @default_line_width.setter
    def default_line_width(self, value: float):
        glLineWidth(value)
        self._default_line_width = value
    
    def clear(self):
        """Clears the framebuffer."""
        glClearColor(*self.clear_color)
        glClear(GL_COLOR_BUFFER_BIT)

    def draw_points(
            self, 
            points: Iterable[PointType], 
            round: bool=False, 
            default_color: ColorType=colors.BLACK, 
            override_color: ColorType=None
        ):
        """
        Draws a set of points.

        Args:
            points (Iterable[PointType]): The points to be drawn.
            round (bool): Should the points be rouded? Defaults to False.
            default_color (ColorType, optional): A default color used for points without a given color. Defaults to BLACK.
            override_color (ColorType, optional): If set, all points will have this color no matter their given color. Defaults to None.
        """
        if round:
            glEnable(GL_POINT_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBegin(GL_POINTS)
        if override_color:
            # color all at once
            glColor3f(*override_color[:3])

        for p in points:
            # if there is not override
            if override_color is None:
                # if p has a color
                if hasattr(p, 'color') and p.color:
                    glColor3f(*p.color[:3])
                # otherwise use the default
                else:
                    glColor3f(*default_color[:3])
            
            # draw the vertex
            glVertex2f(p[0], p[1])
        glEnd()

        if round:
            glDisable(GL_POINT_SMOOTH)
            glDisable(GL_BLEND)
        
    def draw_cubic_bezier(
            self,
            points: Iterable[Point] | Iterable[set],
            do_smooth: bool=True,
            do_alpha_blend: bool=True, 
            line_width: int=None, 
            line_color: set[float]=colors.BLACK
    ):
        """
        Draws a cubic bezier to the window.

        Args:
            points (Iterable[Point] | Iterable[set[int]]): The 4 control points.
            do_smooth (bool, optional): Should the line be smoothed. Defaults to True.
            do_alpha_blend (bool, optional): Should alpha blending be enabled (use for antialiasing). Defaults to True.
            line_width (int, optional): The width of the line in viewport pixels. Defaults to 2.0.
            line_color (set[float], optional): The color of the line in RGB or RGBA. Defaults to black i.e., (0, 0, 0).
        """
        assert len(points) == 4, f"must provide exactly 4 points, received {len(points)}"

        # generate the points
        points = _get_cubic_bezier_points(points)

        # draw the polyline
        self.draw_polyline(points, do_smooth, do_alpha_blend, line_width, line_color)

    def draw_polyline(
            self, 
            points: Iterable[Point] | Iterable[set], 
            do_smooth: bool=True, 
            do_alpha_blend: bool=True, 
            line_width: int=None, 
            line_color: set[float]=colors.BLACK
        ):
        """
        Draws a polyline.

        Args:
            points (Iterable[Point] | Iterable[set[int]]): the list of points in the polyline.
            do_smooth (bool, optional): Should the line be smoothed. Defaults to True.
            do_alpha_blend (bool, optional): Should alpha blending be enabled (use for antialiasing). Defaults to True.
            line_width (int, optional): The width of the line in viewport pixels. Defaults to 2.0.
            line_color (set[float], optional): The color of the line in RGB or RGBA. Defaults to black i.e., (0, 0, 0).
        """
        if do_smooth:
            glEnable(GL_LINE_SMOOTH)
        if do_alpha_blend:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # set line width if given
        if line_width:
            glLineWidth(line_width)

        glColor3f(*line_color[:3])

        # draw line
        glBegin(GL_LINE_STRIP)
        for p in points:
            glVertex2f(p._x, p._y)
        glEnd()

        # reset the line width to the default one
        glLineWidth(self.default_line_width)

    def draw_lines(points: Iterable[PointType], color: ColorType=colors.BLACK):
        glColor3f(*color[:3])

        glBegin(GL_LINES)
        for point in points:
            glVertex2f(*point)
        glEnd()

    def draw_dotted_lines(
            self,
            points: Iterable[PointType], 
            color: ColorType=colors.BLACK,
            scale_factor: float = 1,
            stippled_pattern: int = 0b1010101010101010
        ):
        """
        Draws a dotted line to the window.

        Args:
            points (Iterable[PointType]): The points describing the line. Pairs of points form a line.
            color (ColorType, optional): The color of the line. Defaults to black.
            scaleFactor (float, optional): The segment length, higher means longer. Defaults to 1.
            stipplePattern (int, optional): A 16-bit binary pattern where 1s represent drawn pixels and 0s represent gaps.. Defaults to 0b1010101010101010.
        """
        glColor3f(*color[:3])

        glEnable(GL_LINE_STIPPLE)
        glLineStipple(scale_factor, stippled_pattern)

        glBegin(GL_LINES)
        for point in points:
            glVertex2f(*point)
        glEnd()

        glDisable(GL_LINE_STIPPLE)

def _get_cubic_bezier_points(
            points: Iterable[Point] | Iterable[set], 
            num_segments: int=200,
            return_type: type=Point
            ) -> list[Point] | list[set]:
        """
        Helper func that generates a number of points along a bezier curve given the control points.

        Args:
            points (Iterable[Point] | Iterable[set]): The control points. Length must be 4.
            num_segments (int, optional): How many output points. Defaults to 200.
            return_type (type, optional): Should the function return Points or coordinates in sets. Defaults to Point.

        Raises:
            ValueError: if return_type is neither Point nor set.

        Returns:
            list[Point] | list[set[int]]: The list of points along the bezier curve.
        """
        assert len(points) == 4, "num of control points must be 4 for cubic bezier"

        p0, p1, p2, p3 = points
        
        def bez(t, a, b, c, d):
            return (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
        
        # generate the points first
        curve_points = []
        if return_type is Point:
            for i in range(num_segments + 1):
                t = i / num_segments
                x = bez(t, p0[0], p1[0], p2[0], p3[0])
                y = bez(t, p0[1], p1[1], p2[1], p3[1])
                curve_points.append(Point(x, y))
        elif return_type is set:
            for i in range(num_segments + 1):
                t = i / num_segments
                x = bez(t, p0[0], p1[0], p2[0], p3[0])
                y = bez(t, p0[1], p1[1], p2[1], p3[1])
                curve_points.append((x, y))
        else:
            raise ValueError("param return_type must be Point or set")
        
        return curve_points
