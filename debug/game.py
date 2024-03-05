import pymunk
import pyxel
import math
from pyxel_draw_options import PyxelDrawOptions


WIDTH = 300
HEIGHT = 300
FPS = 30


class App:

    def __init__(self):

        pyxel.init(width=WIDTH, height=HEIGHT, fps=FPS)

        self.options = PyxelDrawOptions()

        self.space = pymunk.Space()
        self.space.gravity = (0, 98)

        f = pymunk.Body(body_type=pymunk.Body.STATIC)
        f.position = (0, 0)

        # borders
        thickness = 8
        bt = pymunk.Segment(f, (0, 0), (WIDTH - 1, 0), thickness)
        bl = pymunk.Segment(f, (0, 0), (0, HEIGHT - 1), thickness)
        br = pymunk.Segment(f, (WIDTH - 1, 0), (WIDTH - 1, HEIGHT - 1), thickness)
        bb = pymunk.Segment(f, (0, HEIGHT - 1), (WIDTH - 1, HEIGHT - 1), thickness)

        borders = [bt, bl, br, bb]

        for border in borders:
            border.elasticity = 0.5
            border.friction = 0.5

        quart = int(WIDTH / 4)

        s1 = pymunk.Segment(f, (0, quart), (quart * 2, quart * 2), 6)
        s2 = pymunk.Segment(f, (quart * 4, quart * 2), (quart * 2, quart * 3), 3)
        s3 = pymunk.Segment(f, (0, quart * 3), (quart * 2, quart * 4), 0)

        segments = [s1, s2, s3]

        for segment in segments:
            segment.elasticity = 0.5
            segment.friction = 0.5

        circles = []
        for i in range(23):

            radius = max(3, int(i / 2))
            mass = radius * 100
            inertia = pymunk.moment_for_circle(radius, 0, radius, (0, 0))

            b1 = pymunk.Body(mass, inertia)
            b1.position = 15 + (radius * i), 25

            c1 = pymunk.Circle(b1, radius)
            c1.elasticity = 0.5
            c1.friction = 0.5

            circles = circles + [b1, c1]


        rects = []
        w, h = 15, 10
        radius = 4
        mass = 100
        for i in range(5):

            vs = [(round(a), round(b)) for a, b in [(-w/2,-h/2), (w/2,-h/2), (w/2,h/2), (-w/2,h/2)]]
            inertia = pymunk.moment_for_poly(mass=mass, vertices=vs, radius=radius)

            b1 = pymunk.Body(mass, inertia)
            b1.position = 50 + (radius * i), 45

            c1 = pymunk.Poly(b1, vs, radius=radius)

            c1.elasticity = 0.5
            c1.friction = 0.5

            rects = rects + [b1, c1]


        polys2 = []
        
        v_radius = 10
        radius = 1
        mass = 100
        for i in range(8):

            num_vertices = max(3, i)

            angle_increment = 2 * math.pi / num_vertices

            # Calcola le coordinate dei vertici del poligono
            polygon_vertices = [
                (v_radius * math.cos(i * angle_increment), v_radius * math.sin(i * angle_increment))
                for i in range(num_vertices)
            ]
            inertia = pymunk.moment_for_poly(mass=mass, vertices=polygon_vertices, radius=radius)
            b1 = pymunk.Body(mass, inertia)
            b1.position = 50 + (v_radius * i), 55

            c1 = pymunk.Poly(b1, polygon_vertices, radius=radius)
            c1.elasticity = 0.5
            c1.friction = 0.5
            polys2 = polys2 + [b1, c1]

        
        self.space.add(f, *borders, *segments, *rects, *circles, *polys2)

        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.space.step(1 / FPS)


    def draw(self):
        pyxel.cls(0)
        self.space.debug_draw(self.options)


App()

