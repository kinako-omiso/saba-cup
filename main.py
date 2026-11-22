import json
import random
from dataclasses import dataclass

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
        with open("data/books.json", encoding="utf-8") as books_file:
            self.books = [Book(**book) for book in json.load(books_file)]
        random.shuffle(self.books)
        self.book_index = 0
        ## jsonファイルから本の情報を読み込む処理はここまで

        pyxel.init(
            setting.GAME_WINDOW_WIDTH,
            setting.GAME_WINDOW_HIGH,
            title=setting.TITLE_NAME,
            display_scale=1,
        )
        pyxel.colors[:] = list(pyxel.colors) + GameScene.BATTLE_PALETTE

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
            title = "TITLE"
            pyxel.text((setting.GAME_WINDOW_WIDTH - len(title) * 4) // 2, 50, title, 7)
            label = "START"
            pyxel.text(
                (setting.GAME_WINDOW_WIDTH - len(label) * 4) // 2,
                self.title_button.y + (self.title_button.h - 6) // 2,
                label,
                7,
            )
        elif self.state == self.BATTLE:
            GameScene.draw(self)
        elif self.state == self.RESULT:
            ResultScene.result_draw(self, self.scores[1], self.scores[2])
        for player in (self.player_1, self.player_2):
            pyxel.circb(player.x, player.y, 10, setting.PLAYER_COLORS[player.num])


    def title_setup(self):
        width, height = 100, 50
        self.title_button = button.Button(
            (setting.GAME_WINDOW_WIDTH - width) // 2,
            (setting.GAME_WINDOW_HIGH - height) // 2,
            width,
            height,
            [self.player_1, self.player_2],
        )
        self.state = self.TITLE

    def battle_setup(self):
        GameScene.setup(self)
        self.state = self.BATTLE

Game()
