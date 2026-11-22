import json
import random
from dataclasses import dataclass

import pyxel
import GameScene
import ui
import ui_title
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
        with (setting.BASE_PATH / "data/books.json").open(encoding="utf-8") as books_file:
            self.books = [Book(**book) for book in json.load(books_file)]
        random.shuffle(self.books)
        self.book_index = 0
        ## jsonファイルから本の情報を読み込む処理はここまで

        pyxel.init(
            setting.GAME_WINDOW_WIDTH,
            setting.GAME_WINDOW_HIGH,
            title=setting.TITLE_NAME,
            fps=setting.FPS,
            display_scale=1,
        )
        pyxel.colors[:] = list(pyxel.colors) + GameScene.BATTLE_PALETTE
        self.title_image = ui_title.load_image()
        self.covers = GameScene.load_covers(self.books)

        self.player_1 = player.Player(self, 1)
        self.player_2 = player.Player(self, 2)

        self.ui = ui.UI(self.books)
        self.title_setup()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player_1.update()
        self.player_2.update()

        # シーン別処理
        if self.state == self.TITLE:
            for b in self.buttons.values():
                b.update()
            if self.buttons["start"].pushed != 0:
                self.battle_setup()
        elif self.state == self.BATTLE:
            if GameScene.update(self):
                ResultScene.setup(self)
                self.state = self.RESULT
        elif self.state == self.RESULT:
            ResultScene.result_update(self)

    def draw(self):
        # シーン別処理
        if self.state == self.TITLE:
            ui_title.draw(self.title_image)
            self.ui.draw_buttons(self.buttons)
        elif self.state == self.BATTLE:
            GameScene.draw(self)
        elif self.state == self.RESULT:
            pyxel.cls(0)
            ResultScene.result_draw(self, self.scores[1], self.scores[2])
        for player in (self.player_1, self.player_2):
            pyxel.circb(player.x, player.y, 10, setting.PLAYER_COLORS[player.num])

    def title_setup(self):
        layout = ui_title.title_button_layout()
        self.buttons = {
            name: button.Button(user=[self.player_1, self.player_2], **layout[name])
            for name in ("start",)
        }
        self.state = self.TITLE

    def battle_setup(self):
        GameScene.setup(self)
        self.state = self.BATTLE

Game()
