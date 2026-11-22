import pyxel
import setting

normal_font = pyxel.Font(str(setting.FONT_PATH), 12)


class AdvancedTextBox:

    def __init__(self, x, y, w, h, c, size, s=15, back_c=0,auto=True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
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

        self.line_layout = [(0, self.w // 2)]
        self.text_use_x = self.w // 2
        self.text_use_y = self.y_h / 2

    def update(self):
        if self.s == 0:
            # 一括表示でも、通常と同じ改行・折り返し処理を最後まで繰り返す。
            while self.text_counter < len(self.text):
                self._draw_next_char()
            return

        if pyxel.frame_count % self.s != 0:
            return

        if self.text_counter >= len(self.text):
            return

        self._draw_next_char()

    def _draw_next_char(self):
        char = self.text[self.text_counter]

        # 改行処理
        if char == "\n":
            self._next_line()

        else:
            # 行に収まらない文字は次の行に表示する。
            line_end, _ = self.line_layout[self.text_lines_count - 1]
            if self.text_counter == line_end:
                self._next_line()

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

    def _next_line(self):
        self.text_use_y += 12
        self.text_lines_count += 1
        _, self.text_use_x = self.line_layout[self.text_lines_count - 1]
        if self.auto_pagination:
            self.set_show_y((self.text_lines_count - 2) * 12)

    def _layout_lines(self):
        # 12pxの文字間隔を保ち、収まる行には左右に1pxずつ余白を確保する。
        columns = max(1, (self.w - 2) // 12)
        layout = []
        start = 0
        for paragraph in self.text.split("\n"):
            for offset in range(0, max(1, len(paragraph)), columns):
                line = paragraph[offset:offset + columns]
                visible = line.strip()
                x = self.w // 2
                if visible:
                    # 行の前後の空白を除いた表示幅で中央位置を決める。
                    width = (len(visible) - 1) * 12 + normal_font.text_width(visible[-1])
                    indent = (len(line) - len(line.lstrip())) * 12
                    x = (self.w - width) // 2 - indent
                layout.append((start + offset + len(line), x))
            start += len(paragraph) + 1
        return layout

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
        self.show_text_y = 0
        self.text_lines_count = 1

        self.line_layout = self._layout_lines()
        _, self.text_use_x = self.line_layout[0]
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
