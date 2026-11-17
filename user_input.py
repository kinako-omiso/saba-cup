import pyxel
import setting

class UserInput:
    def __init__(self, user_num):
        self.user_num = user_num
        self.cursor_x = 0
        self.cursor_y = 0
        self.interaction = False
        self.late_mouse_x = pyxel.mouse_x
        self.late_mouse_y = pyxel.mouse_y


    def update(self):


        if self.user_num == 1:
            if pyxel.btn(pyxel.KEY_W):
                self.cursor_y -= 10
            if pyxel.btn(pyxel.KEY_S):
                self.cursor_y += 10
            if pyxel.btn(pyxel.KEY_A):
                self.cursor_x -= 10
            if pyxel.btn(pyxel.KEY_D):
                self.cursor_x += 10
            if pyxel.btn(pyxel.KEY_LSHIFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
                self.interaction = True
            else:
                self.interaction = False

            axis_x, axis_y = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX), pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)
            if abs(axis_x) > 8000: self.cursor_x += (axis_x / 32768) * 30
            if abs(axis_y) > 8000: self.cursor_y += (axis_y / 32768) * 30

        elif self.user_num == 2:
            if pyxel.btn(pyxel.KEY_UP):
                self.cursor_y -= 10
            if pyxel.btn(pyxel.KEY_DOWN):
                self.cursor_y += 10
            if pyxel.btn(pyxel.KEY_LEFT):
                self.cursor_x -= 10
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.cursor_x += 10
            if pyxel.btn(pyxel.KEY_RSHIFT) or pyxel.btn(pyxel.GAMEPAD2_BUTTON_A) or pyxel.btn(pyxel.GAMEPAD2_BUTTON_B):
                self.interaction = True
            else:
                self.interaction = False

            axis_x, axis_y = pyxel.btnv(pyxel.GAMEPAD2_AXIS_LEFTX), pyxel.btnv(pyxel.GAMEPAD2_AXIS_LEFTY)
            if abs(axis_x) > 8000: self.cursor_x += (axis_x / 32768) * 10
            if abs(axis_y) > 8000: self.cursor_y += (axis_y / 32768) * 10



        else:
            pass


        



