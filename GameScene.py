import random

import pyxel

from Card import Card
from advanced_textbox import AdvancedTextBox, normal_font
from setting import BASE_PATH, FONT_PATH, FPS, GAME_WINDOW_HIGH, GAME_WINDOW_WIDTH, PLAYER_COLORS


CARDS_PER_ROW = 5
CARD_ROWS = 2
CARD_GAP = 12
CARD_ROW_WIDTH = CARDS_PER_ROW * Card.WIDTH + (CARDS_PER_ROW - 1) * CARD_GAP
CARD_ROW_STEP = Card.HEIGHT + CARD_GAP
BATTLE_WIDTH = CARD_ROW_WIDTH + 100
BATTLE_X = (GAME_WINDOW_WIDTH - BATTLE_WIDTH) // 2
VERTICAL_MARGIN = 8
SHELF_BOTTOM_HEIGHT = 14
SHELF_BOTTOM_Y = GAME_WINDOW_HIGH - VERTICAL_MARGIN
CARDS_BOTTOM_Y = SHELF_BOTTOM_Y - SHELF_BOTTOM_HEIGHT
FIRST_CARD_Y = CARDS_BOTTOM_Y - Card.HEIGHT - (CARD_ROWS - 1) * CARD_ROW_STEP
SHELF_TOP_Y = FIRST_CARD_Y - 14
PANEL_HEIGHT = SHELF_TOP_Y - VERTICAL_MARGIN - 4
HINT_LABELS = ("ヒント1", "ヒント2", "答え")
HINT_PAUSE_FRAMES = FPS * 5
READING_PANEL = (BATTLE_X + 20, VERTICAL_MARGIN, BATTLE_WIDTH - 148, PANEL_HEIGHT)
SCORE_PANEL = (BATTLE_X + BATTLE_WIDTH - 116, VERTICAL_MARGIN, 96, PANEL_HEIGHT)
PALETTE_LIMIT = 256

BATTLE_PALETTE = [
    0x292F58, 0x884650, 0xD78445, 0xEEEEEE,
    0xA8BDF6, 0xECC5AE, 0x73C5AB, 0xFF9999, 0xEBC15B,
]
BACKGROUND, SHELF, WOOD, PAPER = range(16, 20)
COVER_COLORS = (20, 21, 22, 23, 24, PAPER, WOOD)
reading_font = pyxel.Font(str(FONT_PATH), 16)
score_font = pyxel.Font(str(FONT_PATH), 20)


def load_covers(books):
    paths = sorted({book.assets for book in books if book.assets})
    palette = list(pyxel.colors)
    cover_colors = set()
    try:
        # include_colors は現在のパレットを画像の色で置き換える。
        for path in paths:
            if _load_cover(path, include_colors=True) is not None:
                cover_colors.update(pyxel.colors)
    finally:
        added_colors = sorted(cover_colors.difference(palette))
        pyxel.colors[:] = palette + added_colors[:PALETTE_LIMIT - len(palette)]

    return {path: _load_cover(path) for path in paths}


def setup(game):
    random.shuffle(game.books)
    game.field_cards = [
        _make_card(game, book, index)
        for index, book in enumerate(game.books[:CARDS_PER_ROW * CARD_ROWS])
    ]
    game.book_index = len(game.field_cards)
    game.reading_index = 0
    panel_x, panel_y, panel_width, panel_height = READING_PANEL
    game.reading_box = AdvancedTextBox(
        panel_x + 12, panel_y + 27, panel_width - 24, panel_height - 28,
        BACKGROUND, 1, s=FPS // 2, back_c=PAPER, auto=False,
        font=reading_font, line_height=17, left_aligned=True,
    )
    if game.books:
        _start_question(game)
    game.scores = {1: 0, 2: 0}
    game.card_confirm_held = {
        player.num: player.interaction for player in (game.player_1, game.player_2)
    }


def _load_cover(assets, *, include_colors=False):
    try:
        return pyxel.Image.from_image(str(BASE_PATH / assets), include_colors=include_colors)
    except Exception:
        return None


def _make_card(game, book, index):
    row, column = divmod(index, CARDS_PER_ROW)
    x = BATTLE_X + 50 + column * (Card.WIDTH + CARD_GAP)
    y = FIRST_CARD_Y + row * CARD_ROW_STEP
    color = COVER_COLORS[(book.id - 1) % len(COVER_COLORS)]
    return Card(book, x, y, game.covers.get(book.assets), color)


def _start_question(game):
    book = game.books[game.reading_index]
    game.hint_texts = (book.opening_hint, book.famous_passage_hint, book.title)
    game.hint_index = 0
    game.hint_switch_frame = None
    game.reading_box.set_text(game.hint_texts[0])


def _update_reading(game):
    frame = pyxel.frame_count
    if game.hint_switch_frame is not None and frame >= game.hint_switch_frame:
        game.hint_index += 1
        game.hint_switch_frame = None
        game.reading_box.set_text(game.hint_texts[game.hint_index])

    box = game.reading_box
    box.update()
    if (
        game.hint_index < len(HINT_LABELS) - 1
        and game.hint_switch_frame is None
        and box.text_counter == len(box.text)
    ):
        game.hint_switch_frame = frame + HINT_PAUSE_FRAMES


def update(game):
    if game.reading_index == len(game.books):
        return True

    # すでに一文字以上表示されている問題だけ、札を取れる。
    answer_book = None
    if game.hint_index > 0 or game.reading_box.text_counter > 0:
        answer_book = game.books[game.reading_index]

    # 同じフレームの選択を集めてから、場のカードを取り除く。
    selections = {}
    for player in (game.player_1, game.player_2):
        was_held = game.card_confirm_held[player.num]
        game.card_confirm_held[player.num] = player.interaction
        if not player.interaction or was_held or answer_book is None:
            continue

        # 決定ボタンを押した瞬間に、正解の札にポインターが重なっているか確認する。
        for index, card in enumerate(game.field_cards):
            if card is None or card.book.id != answer_book.id:
                continue
            if card.contains(player.x, player.y):
                # 同じカードを選んだら中心に近い方を優先する。同距離なら1P。
                priority = (card.distance_squared(player.x, player.y), player.num)
                if index not in selections or priority < selections[index]:
                    selections[index] = priority
            break

    for index, (_, player_num) in selections.items():
        game.field_cards[index] = None
        # 山札が残っていれば、空いた位置に補充して場を10枚に戻す。
        if game.book_index < len(game.books):
            book = game.books[game.book_index]
            game.field_cards[index] = _make_card(game, book, index)
            game.book_index += 1
        # カードを取ったプレイヤーに1点を加える。
        game.scores[player_num] += 1
        game.reading_index += 1
        if game.reading_index == len(game.books):
            return True
        _start_question(game)

    _update_reading(game)
    return False


def draw(game):
    pyxel.cls(BACKGROUND)
    pyxel.rect(*READING_PANEL, PAPER)
    pyxel.rectb(*READING_PANEL, SHELF)
    if game.books:
        panel_x, panel_y, _, _ = READING_PANEL
        label = f"第{game.reading_index + 1}問 / {len(game.books)}  {HINT_LABELS[game.hint_index]}"
        pyxel.text(panel_x + 12, panel_y + 7, label, SHELF, normal_font)
        game.reading_box.draw()

    score_x, score_y, score_width, score_height = SCORE_PANEL
    pyxel.rect(*SCORE_PANEL, PAPER)
    pyxel.rectb(*SCORE_PANEL, SHELF)
    for number in (1, 2):
        row_y = score_y + score_height * (2 * number - 1) // 4 - 11
        color = PLAYER_COLORS[number]
        pyxel.rect(score_x + 10, row_y + 1, 4, 22, color)
        pyxel.text(score_x + 20, row_y + 5, f"{number}P", BACKGROUND, normal_font)
        score = str(game.scores[number])
        score_right = score_x + score_width - 10
        pyxel.text(score_right - score_font.text_width(score), row_y, score, color, score_font)

    shelf_x = BATTLE_X + 28
    shelf_width, shelf_height = BATTLE_WIDTH - 56, SHELF_BOTTOM_Y - SHELF_TOP_Y
    pyxel.rect(shelf_x, SHELF_TOP_Y, 8, shelf_height, WOOD)
    pyxel.rect(shelf_x + shelf_width - 8, SHELF_TOP_Y, 8, shelf_height, WOOD)
    pyxel.rect(shelf_x, SHELF_TOP_Y, shelf_width, 8, SHELF)
    pyxel.rect(shelf_x, FIRST_CARD_Y + Card.HEIGHT, shelf_width, CARD_GAP, SHELF)
    pyxel.rect(shelf_x, CARDS_BOTTOM_Y, shelf_width, SHELF_BOTTOM_HEIGHT, SHELF)
    for card in game.field_cards:
        if card is not None:
            card.draw()
