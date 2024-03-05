import pymunk
import pyxel
import math
from typing import Sequence
from pymunk.space_debug_draw_options import SpaceDebugColor
from pymunk.vec2d import Vec2d



def vec_to_pyxel(a: Vec2d):
    # return int(a[0]), int(a[1])
    # return a[0], a[1]
    return round(a[0]), round(a[1])



class PyxelDrawOptions(pymunk.SpaceDebugDrawOptions):


    COLOR_MAP = {
        SpaceDebugColor(r=44.0, g=62.0, b=80.0, a=255.0): 1,
        SpaceDebugColor(r=149.0, g=165.0, b=166.0, a=255.0): 13,
        SpaceDebugColor(r=231.0, g=76.0, b=60.0, a=255.0): 9,
        SpaceDebugColor(r=52.0, g=152.0, b=219.0, a=255.0): 6
    }


    def __init__(self) -> None:
        """
        Draw a pymunk.Space in a pyxel game.

        Typical usage::

        >>> import pymunk
        >>> from pymunk.space_debug_draw_options import SpaceDebugColor
        >>>
        >>> space = pymunk.Space()
        >>> draw_options = PyxelDrawOptions()
        >>> space.debug_draw(draw_options)
        """

        super(PyxelDrawOptions, self).__init__()


    def draw_circle(
        self,
        pos: pymunk.Vec2d,
        angle: float,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        """
        
        Args:
            pos (pymunk.Vec2d): _description_
            angle (float): _description_
            radius (float): _description_
            outline_color (SpaceDebugColor): _description_
            fill_color (SpaceDebugColor): _description_
        """
        x, y = vec_to_pyxel(pos)

        new_outline = PyxelDrawOptions.COLOR_MAP[outline_color]
        new_fill = PyxelDrawOptions.COLOR_MAP[fill_color]

        radius = round(radius)

        # cerchio pieno
        pyxel.circb(x, y, radius, new_fill)

        # coordinate del punto sulla circonferenza
        circle_edge_x = round(x + radius * math.cos(angle))
        circle_edge_y = round(y + radius * math.sin(angle))

        # raggio di rotazione
        pyxel.line(x, y, circle_edge_x, circle_edge_y, new_outline)



    def draw_segment(
        self,
        a: Vec2d,
        b: Vec2d,
        color: SpaceDebugColor
    ) -> None:
        """

        Args:
            a (Vec2d): _description_
            b (Vec2d): _description_
            color (SpaceDebugColor): _description_
        """
        new_color = PyxelDrawOptions.COLOR_MAP[color]
        xa, ya = vec_to_pyxel(a)
        xb, yb = vec_to_pyxel(b)
        pyxel.line(xa, ya, xb, yb, new_color)



    def draw_fat_segment(
        self,
        a: Vec2d,
        b: Vec2d,
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor
    ):
        """

        Args:
            a (Vec2d): _description_
            b (Vec2d): _description_
            radius (float): _description_
            outline_color (SpaceDebugColor): _description_
            fill_color (SpaceDebugColor): _description_
        """
        # Calcola la lunghezza e l'angolo del segmento

        x1, y1 = vec_to_pyxel(a)
        x2, y2 = vec_to_pyxel(b)

        new_fill_color = PyxelDrawOptions.COLOR_MAP[fill_color]
        new_outline_color = PyxelDrawOptions.COLOR_MAP[outline_color]

        # unico segmento o segmento interno
        pyxel.line(x1, y1, x2, y2, new_fill_color)

        radius = round(radius)

        if radius > 2:

            radius = radius -1

            dx = x2 - x1
            dy = y2 - y1

            # length = math.sqrt(dx**2 + dy**2)
            angle = math.atan2(dy, dx)

            # Calcola le coordinate degli estremi del segmento con spessore
            x1_outer = round(x1 + radius * math.cos(angle + math.pi / 2))
            y1_outer = round(y1 + radius * math.sin(angle + math.pi / 2))
            x1_inner = round(x1 + radius * math.cos(angle - math.pi / 2))
            y1_inner = round(y1 + radius * math.sin(angle - math.pi / 2))

            x2_outer = round(x2 + radius * math.cos(angle + math.pi / 2))
            y2_outer = round(y2 + radius * math.sin(angle + math.pi / 2))
            x2_inner = round(x2 + radius * math.cos(angle - math.pi / 2))
            y2_inner = round(y2 + radius * math.sin(angle - math.pi / 2))

            # corpo del segmento
            pyxel.line(x1_outer, y1_outer, x2_outer, y2_outer, new_outline_color)
            pyxel.line(x1_inner, y1_inner, x2_inner, y2_inner, new_outline_color)

            # estremità tonde
            # print(radius)
            pyxel.circb(x1, y1, radius, new_fill_color)
            pyxel.circb(x2, y2, radius, new_fill_color)



    def draw_polygon(
        self,
        verts: Sequence[Vec2d],
        radius: float,
        outline_color: SpaceDebugColor,
        fill_color: SpaceDebugColor,
    ) -> None:
        """
        
        Args:
            verts (Sequence[Vec2d]): _description_
            radius (float): _description_
            outline_color (SpaceDebugColor): _description_
            fill_color (SpaceDebugColor): _description_
        """
        points = [vec_to_pyxel(v) for v in verts]
        points += [points[0]]

        radius = round(radius)

        new_fill_color = PyxelDrawOptions.COLOR_MAP[fill_color]

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            pyxel.line(x1, y1, x2, y2, new_fill_color)

        if radius > 0:
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i + 1) % len(verts)]
                # ricorreggo
                self.draw_fat_segment(a, b, radius + 1, outline_color, fill_color)



    def draw_dot(
        self, size: float, pos: Vec2d, color: SpaceDebugColor
    ) -> None:
        """

        Args:
            size (float): _description_
            pos (Vec2d): _description_
            color (SpaceDebugColor): _description_
        """
        x, y = vec_to_pyxel(pos)
        new_color = PyxelDrawOptions.COLOR_MAP[color]
        pyxel.pset(x, y, new_color)

