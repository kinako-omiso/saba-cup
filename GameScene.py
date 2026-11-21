def update(game):
    if game.book_index < len(game.books):
        print(game.books[game.book_index].id)
        game.book_index += 1
    if game.book_index == len(game.books):
        game.state = game.RESULT
