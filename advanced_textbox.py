import pyxel

FONT_PATH = "fonts/PixelMplus12-Regular.ttf"
normal_font = pyxel.Font(FONT_PATH, 12)


class AdvancedTextBox:

    def __init__(self, x, y, w, h, c, size, s=15, back_c=0,auto=True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x_w = self.w//12
        self.y_h = self.h//12
        self.text = ""
        self.text_counter = 0
        self.c = c
        self.size = size

        self.s = s ## 表示するフレーム間隔
        self.back_c = back_c
        self.auto_pagination = auto

        self.show_text_y = 0
        self.text_lines_count = 1

        self.img = pyxel.Image(w, h * 5)
        self.img.cls(self.back_c)

        self.text_use_x = self.x_w / 2 -2
        self.text_use_y = self.y_h / 2

    def update(self):
        if self.s == 0:
            self.img.text(self.text_use_x, self.text_use_y, self.text, self.c, normal_font)
            return

        if pyxel.frame_count % self.s != 0:
            return

        if self.text_counter >= len(self.text):
            return

        char = self.text[self.text_counter]

        # 改行処理
        if char == "\n":
            self.text_use_x = self.x_w / 2 -2
            self.text_use_y += 12
            self.text_lines_count += 1
            if self.auto_pagination:
                self.set_show_y((self.text_lines_count - 2) * 12)

        else:
            # 描画位置が右端を超える場合は折り返す
            if self.text_use_x + 12 > self.w:
                self.text_use_x = self.x_w / 2 -2
                self.text_use_y += 12
                self.text_lines_count += 1
                if self.auto_pagination:
                    self.set_show_y((self.text_lines_count - 2) * 12)
                    

            # 文字を画像に追加
            self.img.text(
                self.text_use_x,
                self.text_use_y,
                char,
                self.c,
                normal_font
            )


            self.text_use_x += 12

        self.text_counter += 1

    def draw(self):

        pyxel.blt(
            self.x, self.y,
            self.img,
            0, self.show_text_y,
            self.w, self.h,
            None,
            scale=self.size
        )

    def set_text(self, text):
        self.text = text
        self.text_counter = 0

        self.text_use_x = self.x_w / 2 - 2
        self.text_use_y = self.y_h / 2

        # 前の文字を消去
        self.img.cls(self.back_c)


    def set_show_y(self, v):
        if self.h < self.text_lines_count * 12:
            self.show_text_y = v
        if 0 > self.show_text_y:
            self.show_text_y = 0
        elif self.h * 5 < self.show_text_y:
            self.show_text_y = self.h * 5



       
            