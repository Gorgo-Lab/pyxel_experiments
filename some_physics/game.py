import random
import pyxel
import math
import pymunk
from pyxel_draw_options import PyxelDrawOptions


WIDTH = 128
HEIGHT = 128
FPS = 30
TILE_WIDTH = 8

BALL_NUM = 30
ELASTICITY = 0.9    # divertente se = 1
GRAVITY = (0, 98)



def draw_rotated_square(x, y, angle, side_length, color):
    # coordinate degli angoli del quadrato non ruotato
    half_length = side_length / 2
    angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]

    # coordinate degli angoli
    rotated_angles = [a + angle - math.radians(45) for a in angles]

    # coordinate degli angoli ruotati
    square_vertices = [(x + half_length * math.cos(a), y + half_length * math.sin(a)) for a in rotated_angles]

    # quattro lati ruotati
    pyxel.line(square_vertices[0][0], square_vertices[0][1], square_vertices[1][0], square_vertices[1][1], color)
    pyxel.line(square_vertices[1][0], square_vertices[1][1], square_vertices[2][0], square_vertices[2][1], color)
    pyxel.line(square_vertices[2][0], square_vertices[2][1], square_vertices[3][0], square_vertices[3][1], color)
    pyxel.line(square_vertices[3][0], square_vertices[3][1], square_vertices[0][0], square_vertices[0][1], color)



class World:

    def __init__(self):

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (0, 0)

        # aggiustato a mano :(
        BORDER_THICKNESS = 8
        BORDER_FRICTION = 0.8
        BODER_ELASTICITY = ELASTICITY
        HALF_TILE = TILE_WIDTH / 2

        # borders

        bt = pymunk.Segment(self.body, (0, 0), (WIDTH - 1, 0), BORDER_THICKNESS)
        bl = pymunk.Segment(self.body, (0, 0), (0, HEIGHT - 1), BORDER_THICKNESS)
        br = pymunk.Segment(self.body, (WIDTH - 1, 0), (WIDTH - 1, HEIGHT - 1), BORDER_THICKNESS)
        bb = pymunk.Segment(self.body, (0, HEIGHT - 1), (WIDTH - 1, HEIGHT - 1), BORDER_THICKNESS)

        self.borders = [bt, bl, br, bb]

        for border in self.borders:
            border.elasticity = BODER_ELASTICITY
            border.friction = BORDER_FRICTION

    def register(self, space):
        space.add(self.body, *self.borders)

    def update(self):
        pass

    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)



class PhysicBall:

    def __init__(self, x, y, radius):
        self.radius = radius

        mass = self.radius

        self.x = x
        self.y = y

        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))

        self.body = pymunk.Body(mass, inertia)
        self.body.position = self.x, self.y
        
        foo = 200
        self.body.velocity = random.randint(-foo, foo), random.randint(-foo, foo)

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = ELASTICITY
        self.shape.friction = ELASTICITY

    def register(self, space):
        space.add(self.body, self.shape)



class Ball:

    def __init__(self, physicBall, colore):
        self.physicBall = physicBall
        self.x, self.y = self.physicBall.body.position

        self.radius = self.physicBall.radius
        self.colore = colore

    def update(self):
        # fetch position from physical world
        self.x = round(self.physicBall.body.position[0])
        self.y = round(self.physicBall.body.position[1])

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.colore)
        # riflesso
        pyxel.circb(self.x + self.radius / 2, self.y - self.radius / 2, 1, 13)



class PhysicThwomp: 

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mass = 500
        self.radius = 4
        self.side_length = 32

        w, h = round(self.side_length / 2), round(self.side_length / 2)
        vs = [(round(a), round(b)) for a, b in [(-w/2,-h/2), (w/2,-h/2), (w/2,h/2), (-w/2,h/2)]]

        inertia = pymunk.moment_for_poly(mass=self.mass, vertices=vs, radius=self.radius)

        self.body = pymunk.Body(self.mass, inertia)
        self.body.position = self.x, self.y

        self.shape = pymunk.Poly(self.body, vs, radius=self.radius)
        self.shape.elasticity = 0.2
        self.shape.friction = 0.8

        foo = 25
        self.body.velocity = random.randint(-foo, foo), random.randint(-foo, foo)

    def register(self, space):
        space.add(self.body, self.shape)



class Thwomp:

    def __init__(self, physicThwomp, colore):
        self.physicThwomp = physicThwomp
        self.colore = colore
        self.x, self.y = self.physicThwomp.body.position

    def update(self):
        # fetch position from physical world
        self.x = round(self.physicThwomp.body.position[0])
        self.y = round(self.physicThwomp.body.position[1])

    def draw(self):
        draw_rotated_square(self.x, self.y, self.physicThwomp.body.angle, self.physicThwomp.side_length, self.colore)
        pyxel.fill(self.x, self.y, self.colore)
        pyxel.blt(self.x - 4, self.y - 4, 0, 8, 0, 8, 8, 1)


class App:


    def __init__(self):
        pyxel.init(width=WIDTH, height=HEIGHT, fps=FPS)
        pyxel.load("assets/assets.pyxres")

        self.draw_options = PyxelDrawOptions()
        self.toggle_draw_debug = False

        # space fisico
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY

        # generazione del mondo (bordi e ostacoli)
        self.world = World()
        self.world.register(self.space)

        # generazione delle ball
        self.palle = []
        for _ in range(BALL_NUM):

            radius = random.randint(2, 5)
            margin = TILE_WIDTH + radius
            color = random.choice([1, 2, 5, 6, 8, 12, 13])

            # physic balls
            ppalla = PhysicBall(random.randint(margin, WIDTH - margin), random.randint(margin, HEIGHT - margin), radius)
            ppalla.register(self.space)

            # sprite ball
            palla = Ball(ppalla, color)
            self.palle.append(palla)

        # generazione dei thwomp
        pthwomp = PhysicThwomp(WIDTH / 2, HEIGHT / 2)
        pthwomp.register(self.space)
        self.thwomp = Thwomp(pthwomp, 11)

        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_H):
            self.toggle_draw_debug = not self.toggle_draw_debug

        # aggiorno la fisica
        self.space.step(1 / FPS)

        # aggiorno il mondo
        self.world.update()

        # aggiorno le balls
        for palla in self.palle:
            palla.update()

        # aggiorno il thwomp
        self.thwomp.update()


    def draw(self):
        pyxel.cls(0)

        if self.toggle_draw_debug:
            self.space.debug_draw(self.draw_options)
        else:
            # disegno il mondo
            self.world.draw()

            # disegno le balls
            for palla in self.palle:
                palla.draw()

            # disegno i thwomp
            self.thwomp.draw()

        # testo
        str = "On" if self.toggle_draw_debug else "Off"
        pyxel.text(10, 10, f"(H) Debug: {str}", 7)


App()