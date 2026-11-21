from Card import Card


CARDS_PER_ROW = 5
CARD_ROWS = 2


def setup(game):
    # Issue #5 の処理で読み込んだ本のデータから、5列×2行にカードを配る。
    game.field_cards = [
        Card(book, *_card_position(index))
        for index, book in enumerate(game.books[:CARDS_PER_ROW * CARD_ROWS])
    ]
    game.book_index = len(game.field_cards)
    game.scores = {1: 0, 2: 0}
    game.card_confirm_held = {
        player.num: player.interaction for player in (game.player_1, game.player_2)
    }
    # 場の座標と、その位置にあるカードのタイトルを確認する。
    for card in game.field_cards:
        print(f"({card.x}, {card.y}) {card.book.title}")


def _card_position(index):
    row, column = divmod(index, CARDS_PER_ROW)
    return 40 + column * 108, 80 + row * 148


def update(game):
    # 同じフレームの選択を集めてから、場のカードを取り除く。
    selections = {}
    for player in (game.player_1, game.player_2):
        was_held = game.card_confirm_held[player.num]
        game.card_confirm_held[player.num] = player.interaction
        if not player.interaction or was_held:
            continue

        # 決定ボタンを押した瞬間に、ポインターが重なっているカードを探す。
        for index, card in enumerate(game.field_cards):
            if card is not None and card.contains(player.x, player.y):
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
            card = Card(book, *_card_position(index))
            game.field_cards[index] = card
            game.book_index += 1
            print(f"({card.x}, {card.y}) {card.book.title}")
        # カードを取ったプレイヤーに1点を加える。
        game.scores[player_num] += 1
        print(f"1P: {game.scores[1]}  2P: {game.scores[2]}")

    # TODO(#8): ゲームの終了を判定し、リザルト画面へ遷移する。


def draw(game):
    for card in game.field_cards:
        if card is not None:
            card.draw()
    # TODO(#8): #3 のテキスト表示処理で、入力されたテキストを画面に表示する。
