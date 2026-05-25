import pyxel
from constants import *

class App:
    def __init__(self) -> None:
        pyxel.init(128, 128, title="Jumpy", fps=60)
        pyxel.load("assets.pyxres")
        self.player = Player(64, 0, 16, 16, 0, 8)

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        self.player.update()

    def draw(self) -> None:
        pyxel.cls(6)
        self.player.draw()

class Player:
    def __init__(
        self,
        x: float,
        y: float,
        w: int,
        h: int,
        u: int,
        v: int,
        jump_power: float = 6,
        movement_speed: float = 3,
    ) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.u = u
        self.v = v
        self.vel_x = 0
        self.vel_y = 0
        self.in_air = False
        self.crouching = False
        self.crouch_frame = 0
        self.jump_power = 6
        self.movement_speed = 3

    def update(self) -> None:
        #print(self.x, self.y, self.vel_y)
        vel_x = self.vel_x
        if self.vel_x != 0:
            self.vel_x = max(0, self.vel_x - .5) if self.vel_x > 0 else min(0, self.vel_x + .5)
        if self.vel_y < 0:
            self.vel_y = min(0, self.vel_y + GRAVITY_STRENGTH)

        if self.y < 64:
            self.in_air = True
            self.vel_y = min(self.jump_power, self.vel_y + GRAVITY_STRENGTH)
        else:
            self.in_air = False

        if pyxel.btnp(pyxel.KEY_S) and not self.in_air:
            self.crouch_frame = pyxel.frame_count
            self.crouching = True
        if pyxel.btnr(pyxel.KEY_S) and not self.in_air:
            self.crouching = False

        if self.in_air and self.crouching:
            self.crouching = False

        vel_x_multiplier = 1
        if self.crouching:
            vel_x_multiplier = .5

        self.x += self.vel_x * vel_x_multiplier
        self.x = max(0, self.x)
        self.x = min(pyxel.width - self.w, self.x)
        self.y = min(self.y + self.vel_y, 64)

        if self.y == 64:
            self.vel_y = 0

        if pyxel.btn(pyxel.KEY_Q):
            self.vel_x = -self.movement_speed
        if pyxel.btn(pyxel.KEY_D):
            self.vel_x = self.movement_speed
        if pyxel.btn(pyxel.KEY_SPACE) and not self.in_air:
            self.vel_y = -self.jump_power

    def draw(self) -> None:
        u = self.u
        v = self.v
        offset_u = 0
        if self.vel_x > 0:
            offset_u = (pyxel.frame_count // 8 % 4) * 16

        if self.vel_x < 0:
            offset_u = 64 + (pyxel.frame_count // 8 % 4) * 16

        if self.vel_y != 0 and self.vel_x >= 0:
            if self.vel_y > 2.5:
                offset_u = 48
            else:
                offset_u = 32
        elif self.vel_y != 0 and self.vel_x < 0:
            if self.vel_y > 2.5:
                offset_u = 80
            else:
                offset_u = 96

        if self.crouching:
            v = 40
            if self.vel_x >= 0:
                offset_u = min(3, (pyxel.frame_count - self.crouch_frame) // 8) * 16
            else:
                offset_u = 64 + min(3, (pyxel.frame_count - self.crouch_frame) // 8) * 16


        u += offset_u
        #print(u, v, self.crouching)
        pyxel.blt(
            self.x,
            self.y,
            0,
            u,
            v,
            self.w,
            self.h,
            5
        )
