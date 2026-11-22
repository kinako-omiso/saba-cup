import pyxel
import ui

class Button:
    BOTH_PLAYERS = 3

    def __init__(self, x, y, w, h, user, img=[], act=True, label="", align="left", valign="top", label_scale=2):

        self.x, self.y = ui.aligned_position(x, y, w, h, align, valign)
        self.w = w
        self.h = h
        self.user = user
        self.img = img
        self.act = act
        self.label = label
        self.label_scale = label_scale
        self.pushed = 0
        self.ui_is_on = False


    def update(self):
        if self.act:
            self.ui_is_on = False
            self.pushed = 0
            first_time = float("inf")
    
            for u in self.user:
                if self.x <= u.x <= self.x + self.w and self.y <= u.y <= self.y + self.h:
                    self.ui_is_on = True
    
                    if u.interaction:
                        if u.interaction_time < first_time:
                            first_time = u.interaction_time
                            self.pushed = u.num
    
                        elif u.interaction_time == first_time:
                            self.pushed = self.BOTH_PLAYERS




    def draw(self):

        if self.ui_is_on:
            pyxel.rectb(self.x - 1, self.y - 1, self.w + 2, self.h + 2, 10)
        
        if self.img == []:
            pyxel.rect(self.x, self.y, self.w, self.h, 4)
        pyxel.rectb(self.x, self.y, self.w, self.h, 15)
        if self.label:
            n = self.label_scale
            ui.draw_text(self.x + self.w // 2, self.y + self.h // 2, n, self.label, 7,
                         align="center", valign="center")
