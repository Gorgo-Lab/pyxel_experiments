import random
import pyxel
import pymunk


WIDTH = 128
HEIGHT = 128
FPS = 30
TILE_WIDTH = 8

BALL_NUM = 30
ELASTICITY = 0.9    # divertente se = 1
GRAVITY = (0, 98)


class World:

    def __init__(self):

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (0, 0)

        # aggiustato a mano :(
        BORDER_THICKNESS = 5
        BODER_ELASTICITY = ELASTICITY
        HALF_TILE = TILE_WIDTH / 2

        # borders
        self.borders = []

        top = pymunk.Segment(self.body, (HALF_TILE, HALF_TILE), (WIDTH - HALF_TILE, HALF_TILE), BORDER_THICKNESS)
        left = pymunk.Segment(self.body, (HALF_TILE, HALF_TILE), (HALF_TILE, HEIGHT - 4), BORDER_THICKNESS)
        bottom = pymunk.Segment(self.body, (WIDTH - HALF_TILE, HEIGHT - 4), (HALF_TILE, HEIGHT - HALF_TILE), BORDER_THICKNESS)
        right = pymunk.Segment(self.body, (WIDTH - HALF_TILE, HEIGHT - HALF_TILE), (WIDTH - HALF_TILE, HALF_TILE), BORDER_THICKNESS)

        self.borders = [top, left, bottom, right]

        for border in self.borders:
            border.elasticity = BODER_ELASTICITY

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



class App:

    def __init__(self):
        pyxel.init(width=WIDTH, height=HEIGHT, fps=FPS)
        pyxel.load("assets/assets.pyxres")

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

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # aggiorno la fisica
        self.space.step(1 / FPS)

        # aggiorno il mondo
        self.world.update()

        # aggiorno le balls
        for palla in self.palle:
            palla.update()

    def draw(self):
        pyxel.cls(0)
        
        # disegno il mondo
        self.world.draw()

        # disegno le balls
        for palla in self.palle:
            palla.draw()


App()