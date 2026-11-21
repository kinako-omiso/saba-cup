from Card import Card


CARDS_PER_ROW = 5
CARD_ROWS = 2


def setup(game):
    game.field_cards = [
        Card(book, *_card_position(index))
        for index, book in enumerate(game.books[:CARDS_PER_ROW * CARD_ROWS])
    ]
    game.book_index = len(game.field_cards)
    game.scores = {1: 0, 2: 0}
    game.card_confirm_held = {
        player.num: player.interaction for player in (game.player_1, game.player_2)
    }
    for card in game.field_cards:
        print(card.book.title)


def _card_position(index):
    row, column = divmod(index, CARDS_PER_ROW)
    return 40 + column * 108, 80 + row * 148


def update(game):
    selections = {}
    for player in (game.player_1, game.player_2):
        was_held = game.card_confirm_held[player.num]
        game.card_confirm_held[player.num] = player.interaction
        if not player.interaction or was_held:
            continue

        for index, card in enumerate(game.field_cards):
            if card is not None and card.contains(player.x, player.y):
                priority = (card.distance_squared(player.x, player.y), player.num)
                if index not in selections or priority < selections[index]:
                    selections[index] = priority
                break

    for index, (_, player_num) in selections.items():
        game.field_cards[index] = None
        game.scores[player_num] += 1
        print(f"1P: {game.scores[1]}  2P: {game.scores[2]}")


def draw(game):
    for card in game.field_cards:
        if card is not None:
            card.draw()
