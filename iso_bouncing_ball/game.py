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

        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        self.frame_counter = (self.frame_counter + 1) % self.animation_speed
        if self.frame_counter == 0:
            self.frame = (self.frame + 1) % self.animation_frames


    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.px = max(self.px - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.px = min(self.px + 2, pyxel.width - 16)
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.py = max(self.py - 2, 0)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.py = min(self.py + 2, pyxel.height - 16)


    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)
        pyxel.blt(self.px, self.py, 0, self.frame * 16, 0, 16, 16,0)     


App()
