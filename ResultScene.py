import pyxel
import setting
import advanced_textbox
import button


result_text_box = None
player_1_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/4 - 43,
                                                setting.GAME_WINDOW_HIGH/3,
                                                86, 30, 3, 2, 1, 0, False)
player_1_box.set_text("PLAYER1 SCORE ")
player_2_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/4 * 3 - 43,
                                                setting.GAME_WINDOW_HIGH/3,
                                                86, 30, 8, 2, 1, 0, False)
player_2_box.set_text("PLAYER1 SCORE ")

score_1_box = None
score_2_box = None

fg_once = True
count = 0
max_count = 0

def update():
    pass

def draw(game, score_1, score_2):

    global fg_once
    global result_text_box
    global count
    global max_count
    global player_1_box
    global player_2_box
    global score_1_box
    global score_2_box

    if fg_once:
        game.test_buttons = {
            "retry" : button.Button(setting.GAME_WINDOW_WIDTH/4 -120, setting.GAME_WINDOW_HIGH/4*3,
                                    240, 80, [game.player_1, game.player_2], [], False),
            "quit" : button.Button(setting.GAME_WINDOW_WIDTH/4*3 -120, setting.GAME_WINDOW_HIGH/4*3,
                                    240, 80, [game.player_1, game.player_2], [], False),
        }
        score_1_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/4 ,
                                                       setting.GAME_WINDOW_HIGH/2,
                                                       len(str(score_1))*12 + 2, 14, 10, 6, 1, 0, False)
        score_1_box.set_text(str(score_1))
        score_1_box.text_use_x += 3
        score_2_box = advanced_textbox.AdvancedTextBox(setting.GAME_WINDOW_WIDTH/4*3 ,
                                                       setting.GAME_WINDOW_HIGH/2,
                                                       len(str(score_2))*12 + 2, 14, 10, 6, 1, 0, False)
        score_2_box.set_text(str(score_2))
        score_2_box.text_use_x += 3

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
            result_text_box.text_use_x += 2

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
        for name, b in game.test_buttons.items():
            b.act = True




    
    
    

        