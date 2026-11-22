import json
import random
from dataclasses import dataclass
from pathlib import Path

import pyxel
import GameScene
import ui
import ui_title
import setting
import player
import button


@dataclass
class Book:
    id: int
    title: str
    author: str
    description: str
    opening_hint: str
    famous_passage_hint: str


class Game:

    # ここにシーンを設定
    TITLE = 0
    BATTLE = 1
    RESULT = 2

    def __init__(self):

        ## jsonファイルから本の情報を読み込む
        with (Path(__file__).with_name("data") / "books.json").open(encoding="utf-8") as books_file:
            self.books = [Book(**book) for book in json.load(books_file)]
        random.shuffle(self.books)
        self.book_index = 0
        ## jsonファイルから本の情報を読み込む処理はここまで

        pyxel.init(setting.GAME_WINDOW_WIDTH, setting.GAME_WINDOW_HIGH,
                   title=setting.TITLE_NAME, fps=setting.FPS)

        self.state = self.TITLE
        self.player_1 = player.Player(self, 1)
        self.player_2 = player.Player(self, 2)

        self.ui = ui.UI(self.books)
        self.title_setup()


        pyxel.run(self.update, self.draw)


    def update(self):
        self.player_1.update()
        self.player_2.update()
        for b in self.buttons.values():
            b.update()

        # シーン別処理
        if self.state == self.TITLE:
            if self.buttons["start"].pushed != 0:
                # print("PUSHED", self.buttons["start"].pushed)
                self.state = self.BATTLE
                self.player_select_setup()
        elif self.state == self.BATTLE:
            GameScene.update(self)




      


    def draw(self):
        # シーン別処理
        if self.state == self.TITLE:
            ui_title.draw()
        else:
            pyxel.cls(0)
            if self.state == self.BATTLE:
                pyxel.text(300 - len("BATTLE"), 50, "BATTLE", pyxel.rndi(0,15))

        self.ui.draw_buttons(self.buttons)
        pyxel.circb(self.player_1.x, self.player_1.y, 10, 3)
        pyxel.circb(self.player_2.x, self.player_2.y, 8, 8)


        # if pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
        #     pyxel.text(300, 300, "OK!!", 11)

        # print(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX), pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY))



    def title_setup(self):
        layout = ui_title.title_button_layout()
        self.buttons = {
            name: button.Button(user=[self.player_1, self.player_2], **layout[name])
            for name in ("start",)
        }

    def player_select_setup(self):
        self.buttons = {
            "one" : button.Button(450, 275, 100, 50, [self.player_1, self.player_2]),
        }


Game()
