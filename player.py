import pyxel
import user_input
import setting

class Player():

    def __init__(self, game, num):
        self.game = game
        self.num = num
        self.x = 0
        self.y = 0
        self.interaction = False
        self.user_input = user_input.UserInput(num)

    def update(self):
        self.user_input.update()
        self.x = self.user_input.cursor_x
        self.y = self.user_input.cursor_y
        self.interaction = self.user_input.interaction
        if self.interaction:
            self.interaction_time = pyxel.frame_count

        if self.x <= 0 :
            self.x = 0
        elif self.x >= setting.GAME_WINDOW_WIDTH:
            self.x = setting.GAME_WINDOW_WIDTH
        if self.y <= 0 :
            self.y = 0
        elif self.y >= setting.GAME_WINDOW_HIGH:
            self.y = setting.GAME_WINDOW_HIGH

        #print(self.x, self.y)