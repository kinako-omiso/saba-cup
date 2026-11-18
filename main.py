import pyxel
import setting
import player
import button


class Game:

    # ここにシーンを設定
    TITLE = 0
    BATTLE = 1

    def __init__(self):

        pyxel.init(setting.GAME_WINDOW_WIDTH, setting.GAME_WINDOW_HIGH, title=setting.TITLE_NAME)

        self.state = self.TITLE
        self.player_1 = player.Player(self, 1)
        self.player_2 = player.Player(self, 2)

        self.test_buttons = {
            "one" : button.Button(250, 275, 100, 50, [self.player_1, self.player_2]),
        }


        pyxel.run(self.update, self.draw)


    def update(self):
        for name, b in self.test_buttons.items():
            b.update()

        self.player_1.update()
        self.player_2.update()

        # シーン別処理
        if self.state == self.TITLE:
            if self.test_buttons["one"].pushed != 0:
                print("PUSHED", self.test_buttons["one"].pushed)
                self.state = self.BATTLE
                self.player_select_setup()
        elif self.state == self.BATTLE:
            if self.test_buttons["one"].pushed != 0:
                print("PUSHED", self.test_buttons["one"].pushed)
                self.state = self.TITLE
                self.title_setup()




      


    def draw(self):
        pyxel.cls(0)
        for name, b in self.test_buttons.items():
            b.draw()
        pyxel.circb(self.player_1.x, self.player_1.y, 10, 3)
        pyxel.circb(self.player_2.x, self.player_2.y, 10, 8)

        # シーン別処理
        if self.state == self.TITLE:
            pyxel.text(300 - len("TITLE"), 50, "TITLE", pyxel.rndi(0,15))
        elif self.state == self.BATTLE:
            pyxel.text(300 - len("BATTLE"), 50, "BATTLE", pyxel.rndi(0,15))


        # if pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
        #     pyxel.text(300, 300, "OK!!", 11)

        # print(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX), pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY))



    def title_setup(self):
        self.test_buttons = {
            "one" : button.Button(250, 275, 100, 50, [self.player_1, self.player_2]),
        }

    def player_select_setup(self):
        self.test_buttons = {
            "one" : button.Button(450, 275, 100, 50, [self.player_1, self.player_2]),
        }


Game()