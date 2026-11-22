import pyxel

class Button:
    def __init__(self, x, y, w, h, user, img=[], act=True):

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.user = user
        self.img = img
        self.act = act
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
                            self.pushed = len(self.user) + 1




    def draw(self):
        if self.act:
            if self.ui_is_on:
                pyxel.rectb(self.x - 1, self.y - 1, self.w + 2, self.h + 2, pyxel.rndi(0, 15))

            if self.img == []:
                pyxel.rect(self.x, self.y, self.w, self.h, 13)
            else :
                pyxel.blt(self.x, self.y, self.img, 0, 0, self.w, self.h)