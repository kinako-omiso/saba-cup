import json
import random
from dataclasses import dataclass
from pathlib import Path

import pyxel
import GameScene
import setting
import player
import button
import ResultScene


@dataclass
class Book:
    id: int
    title: str
    author: str
    description: str
    opening_hint: str
    famous_passage_hint: str
    assets: str | None = None


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

        pyxel.init(setting.GAME_WINDOW_WIDTH, setting.GAME_WINDOW_HIGH, title=setting.TITLE_NAME)

        self.player_1 = player.Player(self, 1)
        self.player_2 = player.Player(self, 2)
        self.title_setup()


        pyxel.run(self.update, self.draw)


    def update(self):
        self.player_1.update()
        self.player_2.update()

        # シーン別処理
        if self.state == self.TITLE:
            self.title_button.update()
            if self.title_button.pushed:
                self.battle_setup()
        elif self.state == self.BATTLE:
            if GameScene.update(self):
                ResultScene.setup(self)
                self.state = self.RESULT
        elif self.state == self.RESULT:
            ResultScene.result_update(self)


    def draw(self):
        pyxel.cls(0)

        # シーン別処理
        if self.state == self.TITLE:
            self.title_button.draw()
            pyxel.text(300 - len("TITLE"), 50, "TITLE", pyxel.rndi(0,15))
        elif self.state == self.BATTLE:
            pyxel.text(300 - len("BATTLE"), 50, "BATTLE", pyxel.rndi(0,15))
            GameScene.draw(self)
        elif self.state == self.RESULT:
            ResultScene.result_draw(self, self.scores[1], self.scores[2])
        pyxel.circb(self.player_1.x, self.player_1.y, 10, 3)
        pyxel.circb(self.player_2.x, self.player_2.y, 10, 8)


        # if pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
        #     pyxel.text(300, 300, "OK!!", 11)

        # print(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX), pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY))



    def title_setup(self):
        self.title_button = button.Button(250, 275, 100, 50, [self.player_1, self.player_2])
        self.state = self.TITLE

    def battle_setup(self):
        GameScene.setup(self)
        self.state = self.BATTLE

Game()
