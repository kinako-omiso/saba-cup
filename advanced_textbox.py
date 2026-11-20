import pyxel


normal_font = pyxel.Font("fonts/PixelMplus12-Regular.ttf", 12)

class AdvancedTextBox:

    def __init__(self, x, y, w, h, c, size,s=15):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = ""
        self.use_text = ""
        self.text_counter = 0
        self.c = c
        self.size = size
        self.s = s
        self.img = pyxel.Image(w, h * 5)

    def update(self):
       
        if pyxel.frame_count % self.s == 0:
            if self.text_counter == len(self.text):
                pass
            else:
                self.use_text = self.text[:self.text_counter]
                self.text_counter += 1

        
    def draw(self):
        self.img.cls(0)
        pyxel.text(100, 100, "この文章が表示されるかどうか", 8,normal_font)
        self.img.text(0, 0, self.use_text, self.c, normal_font)
        pyxel.blt(
            self.x, self.y,
            self.img,
            0, 0,
            100, 50,
            0,
            scale=self.size
        )

    def set_text(self, text):
        self.text = text
