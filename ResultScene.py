import pyxel
import setting
import advanced_textbox
import button


result_text_box = None
score_1_box = None
score_2_box = None
retry_text = None
quit_text = None


fg_once = True
count = 0
max_count = 0

def setup(game):
    global fg_once
    global count
    fg_once = True
    count = 0
    game.result_buttons = {}


def result_update(game):
    if not game.result_buttons:
        return

    for b in game.result_buttons.values():
        b.update()

    if game.result_buttons["retry"].pushed:
        game.battle_setup()
    elif game.result_buttons["quit"].pushed:
        game.title_setup()


def result_draw(game, score_1, score_2):

    global fg_once
    global result_text_box
    global count
    global max_count
    global player_1_box
    global player_2_box
    global score_1_box
    global score_2_box
    global retry_text
    global quit_text
    global retry_text_img
    global quit_text_img

    if fg_once:
        player_1_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/4 - 43,
                                                        setting.GAME_WINDOW_HIGH/3,
                                                        86, 30, 3, 2, 1, 0, False)
        player_1_box.set_text("PLAYER1 SCORE ")
        player_2_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/4 * 3 - 43,
                                                        setting.GAME_WINDOW_HIGH/3,
                                                        86, 30, 8, 2, 1, 0, False)
        player_2_box.set_text("PLAYER2 SCORE ")

        retry_text_img = pyxel.Image(280, 80)
        quit_text_img = pyxel.Image(280, 80)

        retry_text = advanced_textbox.AdvancedTextBox(0,0,70,20,8,1,0,6, False)
        retry_text.set_text("もういちど")
        retry_text.update()
        retry_text_img.blt(105,30,retry_text.img,0,0,retry_text.w, retry_text.h, None, scale=4)

        quit_text = advanced_textbox.AdvancedTextBox(0,0,70,20,2,1,0,1, False)
        quit_text.set_text("タイトルへ")
        quit_text.update()
        quit_text_img.blt(105,30,quit_text.img,0,0,quit_text.w, quit_text.h, None, scale=4)
        


        game.result_buttons = {
            "retry" : button.Button(setting.GAME_WINDOW_WIDTH/4 -140, setting.GAME_WINDOW_HIGH/4*3,
                                    280, 80, [game.player_1, game.player_2], retry_text_img, False),
            "quit" : button.Button(setting.GAME_WINDOW_WIDTH/4*3 -140, setting.GAME_WINDOW_HIGH/4*3,
                                    280, 80, [game.player_1, game.player_2], quit_text_img, False),
        }
        score_1_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/4 ,
                                                       setting.GAME_WINDOW_HIGH/2,
                                                       len(str(score_1))*12 + 2, 14, 10, 6, 1, 0, False)
        score_1_box.set_text(str(score_1))
        score_2_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/4*3 ,
                                                       setting.GAME_WINDOW_HIGH/2,
                                                       len(str(score_2))*12 + 2, 14, 10, 6, 1, 0, False)
        score_2_box.set_text(str(score_2))

        result = ""
        if score_1 > score_2:
            result = "PLAYER1  WIN  "
            result_text_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/2 - 43,
                                                               setting.GAME_WINDOW_HIGH/6,
                                                               86, 30, 3, 4, 1, 0, False)
            result_text_box.set_text(result)
        elif score_2 > score_1:
            result = "PLAYER2  WIN  "
            result_text_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/2 - 43,
                                                               setting.GAME_WINDOW_HIGH/6,
                                                               86, 30, 8, 4, 1, 0, False)
            result_text_box.set_text(result)
        else :
            result = "DRAW"
            result_text_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/2 - 25,
                                                               setting.GAME_WINDOW_HIGH/6,
                                                               50, 18, 4, 4, 1, 0, False)
            result_text_box.set_text(result)

        max_count = len(result) + 30
        fg_once = False

    count += 1

    if count < 30 :
     pyxel.rect(0,0,setting.GAME_WINDOW_WIDTH, setting.GAME_WINDOW_HIGH / 30 * count, 0)

    if count == 38:
        result_text_box.c = 10

    if count > 30:
        result_text_box.update()
        result_text_box.draw()

    if count >= max_count:
        player_1_box.update()
        player_2_box.update()
        player_1_box.draw()
        player_2_box.draw()

    if count >= max_count + 14:
        score_1_box.update()
        score_2_box.update()
        score_1_box.draw()
        score_2_box.draw()

    if count == max_count + 17:
        for b in game.result_buttons.values():
            b.act = True

    for b in game.result_buttons.values():
        b.draw()
