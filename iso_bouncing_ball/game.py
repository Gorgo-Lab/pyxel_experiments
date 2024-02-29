import pyxel

class App:
    def __init__(self):
        pyxel.init(128, 128)
        pyxel.load("assets/myRes.pyxres")

        self.px = 0
        self.py = 0
        self.frame = 0
        self.animation_frames = 9  # Assuming 9 frames of animation
        self.animation_speed = 2   # Lower is faster
        self.frame_counter = 0

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        self.frame_counter = (self.frame_counter + 1) % self.animation_speed
        if self.frame_counter == 0:
            self.frame = (self.frame + 1) % self.animation_frames
            if(self.frame == 6):
                pyxel.play(1, pyxel.sounds[0]);

    def update_player(self):

        # To make player move in isometric world both x & y coord must be updated

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.px = max(self.px - 2, 0)
            self.py = max(self.py - 1, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.px = min(self.px + 2, pyxel.width - 16)
            self.py = min(self.py + 1, pyxel.height - 16)
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.py = max(self.py - 1, 0)
            self.px = min(self.px + 2, pyxel.width - 16)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.py = min(self.py + 1, pyxel.height - 16)
            self.px = max(self.px - 2, 0)


    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)
        pyxel.blt(self.px, self.py, 0, self.frame * 16, 0, 16, 16,0)     


App()
