import sys
import pygame_menu
import pygame
import time

xMark = 'X'
oMark = 'O'
player_mark = xMark
cpu_mark = oMark
current_move = player_mark
font = "data/droidsans.ttf"
restart_text = " Press 'r' to restart "


def comp_move(board):
    from copy import deepcopy
    extracted_moves = []
    for x in range(3):
        for y in range(3):
            if board[x][y] is None:
                extracted_moves.append((x, y))

    for i in extracted_moves:
        for symbol in [cpu_mark, player_mark]:
            copy_board = deepcopy(board)
            copy_board[i[0]][i[1]] = symbol
            if is_winner(copy_board, symbol):
                move = i
                return move

    corners = []
    for i in extracted_moves:
        if i in [(0, 0), (2, 0), (0, 2), (2, 2)]:
            corners.append(i)
    if len(corners) > 0:
        move = select_random(corners)
        return move

    if (1, 1) in extracted_moves:
        move = (1, 1)
        return move

    sides = []
    for i in extracted_moves:
        if i in [(1, 0), (2, 1), (1, 2), (0, 1)]:
            sides.append(i)
    if len(sides) > 0:
        move = select_random(sides)
        return move


def select_random(list):
    import random
    length = len(list)
    r = random.randrange(0, length)
    return list[r]


def is_winner(b, s):
    return ((b[0][0] == s and b[0][1] == s and b[0][2] == s) or
            (b[1][0] == s and b[1][1] == s and b[1][2] == s) or
            (b[2][0] == s and b[2][1] == s and b[2][2] == s) or
            (b[0][0] == s and b[1][0] == s and b[2][0] == s) or
            (b[0][1] == s and b[1][1] == s and b[2][1] == s) or
            (b[0][2] == s and b[1][2] == s and b[2][2] == s) or
            (b[0][0] == s and b[1][1] == s and b[2][2] == s) or
            (b[0][2] == s and b[1][1] == s and b[2][0] == s))


def map_mouse_to_board(x, y):
    if x < windowMarginSides + gameSize[0] / 3:
        column = 0
    elif x < (windowMarginSides + gameSize[0] / 3) * 2:
        column = 1
    else:
        column = 2
    if y < (gameSize[1] / 3) + windowMarginTopAndBottom:
        row = 0
    elif y < (gameSize[1] / 3) * 2 + windowMarginTopAndBottom:
        row = 1
    else:
        row = 2
    return column, row


def draw_animated_line(anim):
    start_width = anim[1][0] * gameSize[0] // 3 + windowMarginSides + (gameSize[0] // 3 // 2)
    start_height = anim[1][1] * gameSize[1] // 3 + windowMarginTopAndBottom + (gameSize[1] // 3 // 2)
    anim_width = anim[1][0] * gameSize[0] // 3 + windowMarginSides + (gameSize[0] // 3 // 2)
    anim_height = anim[1][1] * gameSize[1] // 3 + windowMarginTopAndBottom + (gameSize[1] // 3 // 2)
    end_width = anim[3][0] * gameSize[0] // 3 + windowMarginSides + (gameSize[0] // 3 // 2)
    end_height = anim[3][1] * gameSize[1] // 3 + windowMarginTopAndBottom + (gameSize[1] // 3 // 2)

    x = (end_width - anim_width) // 30
    y = (end_height - anim_height) // 30

    for i in range(30):
        if anim_width < end_width:
            anim_width += x
        if anim_height < end_height or anim_height > end_height:
            anim_height += y

        clock.tick(60)
        pygame.draw.line(screen, winColor, (start_width, start_height), (anim_width, anim_height), lineSize)
        pygame.display.flip()


def board_full(board):
    for i in board:
        for j in i:
            if j is None:
                return False
    return True


def move(board, m, symbol):
    # Take board and a move, apply the move to the board
    board[m[0]][m[1]] = symbol


def get_winner(board):
    # Diagonal checking
    win_grid = None
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]) and board[1][1] is not None:
        win_grid = [board[1][1], (0, 0), (1, 1), (2, 2)]
        draw_animated_line(win_grid)
    elif (board[0][2] == board[1][1] and board[1][1] == board[2][0]) and board[1][1] is not None:
        win_grid = [board[1][1], (0, 2), (1, 1), (2, 0)]
        draw_animated_line(win_grid)

    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] is not None:
            win_grid = [board[i][1], (i, 0), (i, 1), (i, 2)]
            draw_animated_line(win_grid)
        elif board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] is not None:
            win_grid = [board[1][i], (0, i), (1, i), (2, i)]
            draw_animated_line(win_grid)

    return win_grid


def draw_board(board):
    my_font = pygame.font.SysFont(font, gameSize[1] // 3)

    for i in range(3):
        for j in range(3):
            x_placement = 0
            y_placement = -50
            if board[i][j] == xMark:
                color = xColor
                x_placement = 75
            else:
                color = oColor
                x_placement = 70

            text_surface = my_font.render(board[i][j], True, color)
            screen.blit(text_surface, (i * (gameSize[0] // 3) + windowMarginSides + x_placement,
                                       j * (gameSize[1] // 3) + windowMarginTopAndBottom-y_placement))


def draw_lines():
    # Vertical lines
    drawing = True
    # start / current / end
    lines = [windowMarginTopAndBottom, windowSize[1] - window_margin_bottom, windowMarginSides,
             windowSize[0] - windowMarginSides]

    while drawing:

        # Vertical
        pygame.draw.line(screen, lineColor, (windowMarginSides + gameSize[0] // 3, windowMarginTopAndBottom),
                         (windowMarginSides + gameSize[0] // 3, lines[0]), lineSize)
        pygame.draw.line(screen, lineColor,
                         (windowMarginSides + (gameSize[0] // 3) * 2, windowSize[1] - window_margin_bottom),
                         (windowMarginSides + (gameSize[0] // 3) * 2, lines[1]), lineSize)

        # Horizontal
        pygame.draw.line(screen, lineColor, (windowMarginSides, windowMarginTopAndBottom + gameSize[1] // 3),
                         (lines[2] - 1, windowMarginTopAndBottom + gameSize[1] // 3), lineSize)
        pygame.draw.line(screen, lineColor,
                         (windowSize[0] - windowMarginSides, windowMarginTopAndBottom + (gameSize[1] // 3) * 2),
                         (lines[3] + 1, windowMarginTopAndBottom + (gameSize[1] // 3) * 2), lineSize)

        if lines[0] <= (windowSize[1] - window_margin_bottom - 2):
            lines[0] += 4
            lines[1] -= 4
        if lines[2] <= (windowSize[0] - windowMarginSides - 5):
            lines[2] += 4
            lines[3] -= 4
        else:
            drawing = False

        clock.tick(120)
        pygame.display.flip()


def won(winner):
    win_font = pygame.font.SysFont(font, 40)
    text = " Winner is {} ".format(winner[0])
    text_width, text_height = win_font.size(text)
    text2_width, text2_height = win_font.size(restart_text)
    win_msg = win_font.render(text, 1, (0, 0, 0), (255, 255, 255))
    win_msg2 = win_font.render(restart_text, 1, (0, 0, 0), (255, 255, 255))
    screen.blit(win_msg,
                (windowSize[0] // 2 - text_width // 2, windowSize[1] // 2 - text_height // 2))
    screen.blit(win_msg2,
                (windowSize[0] // 2 - text2_width // 2, windowSize[1] // 2 + text2_height // 2))


def draw():
    win_font = pygame.font.SysFont(font, 40)
    text = " Draw! "
    text_width, text_height = win_font.size(text)
    text2_width, text2_height = win_font.size(restart_text)
    win_msg = win_font.render(text, 1, (0, 0, 0), (255, 255, 255))
    win_msg2 = win_font.render(restart_text, 1, (0, 0, 0), (255, 255, 255))
    screen.blit(win_msg,
                (windowSize[0] // 2 - text_width // 2, windowSize[1] // 2 - text_height // 2))
    screen.blit(win_msg2,
                (windowSize[0] // 2 - text2_width // 2, windowSize[1] // 2 + text2_height // 2))


def start_game():
    global can_play
    global screen
    global current_move
    screen.fill(backgroundColor)
    board = [[None, None, None], [None, None, None], [None, None, None]]
    if cpu_player is True:
        if current_move is player_mark:
            can_play = True
        else:
            can_play = False

    draw_lines()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = [[None, None, None], [None, None, None], [None, None, None]]
                    screen.fill(backgroundColor)
                    draw_lines()
                    if can_play is False:
                        cpu_move(board)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_F1:
                    open_main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and can_play:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                (column, row) = map_mouse_to_board(mouseX, mouseY)
                if board[column][row] is None:
                    move(board, (column, row), current_move)
                    toggle_current_player()
                    draw_board(board)
                    pygame.display.update()
                    winner = get_winner(board)
                    if winner is not None:
                        won(winner)
                        can_play = False
                    elif board_full(board):
                        draw()
                    elif cpu_player:
                        cpu_move(board)

        win_font = pygame.font.Font(font, 40)
        turn_text = " Turn: {} ".format(current_move)
        text_size = win_font.size(turn_text)
        win_msg = win_font.render(turn_text, 1, (0, 0, 0), (255, 255, 255))
        position = (windowSize[0] // 2 - text_size[0] // 2, windowSize[1] - 2 * 55)
        screen.blit(win_msg, position)
        pygame.display.update()


def cpu_move(board):
    global can_play

    win_font = pygame.font.Font(font, 40)
    wait_text = " AI is thinking... "
    wait_size = win_font.size(wait_text)
    wait = win_font.render(wait_text, 1, (0, 0, 0), (255, 255, 255))
    position2 = (windowSize[0] // 2 - wait_size[0] // 2, windowSize[1] - 2 * 55)
    screen.blit(wait, position2)
    pygame.display.update()
    time.sleep(1.5)
    pygame.draw.rect(screen, backgroundColor, (
        windowSize[0] // 2 - wait_size[0] // 2, windowSize[1] - 2 * 55, wait_size[0]+100,
        55))
    pygame.display.update()
    cpu_move = comp_move(board)
    move(board, cpu_move, current_move)
    draw_board(board)
    toggle_current_player()
    cpu_winner = get_winner(board)
    if cpu_winner is not None:
        won(["AI"])
    if board_full(board):
        draw()


def toggle_current_player():
    global current_move
    global can_play
    if current_move == xMark:
        current_move = oMark
    else:
        current_move = xMark
    if current_move == player_mark:
        can_play = True
    else:
        can_play = False


def toggle_mark():
    global player_mark
    global cpu_player
    global xMark
    global oMark
    global menu

    if player_mark is xMark:
        player_mark = oMark
        cpu_player = xMark
    else:
        player_mark = xMark
        cpu_player = oMark

    menu.get_selected_widget().set_title("Player symbol = {}".format(player_mark))
    pygame.display.update()


def toggle_cpu():
    global cpu_player

    if cpu_player:
        cpu_player = False
        on_off = "off"
    else:
        cpu_player = True
        on_off = "on"

    menu.get_selected_widget().set_title("AI = {}".format(on_off))
    pygame.display.update()


def open_control_menu():
    control_menu = pygame_menu.menu.Menu(300, 400, "Controls", theme=pygame_menu.themes.THEME_DEFAULT)
    control_menu.add_label("Quit = Esc", font_size=20, selectable=False)
    control_menu.add_label("Menu = F1", font_size=20, selectable=False)
    control_menu.add_label(" ", selectable=False)
    control_menu.add_button("Back", open_main_menu, button_id="0")
    control_menu.mainloop(screen)
    control_menu.get_widget("0").set_attribute("active", "True")


def open_main_menu():
    global menu
    if cpu_player:
        on_off = "on"
    else:
        on_off = "off"
    menu = pygame_menu.Menu(400, 500, 'TicTacToe', theme=pygame_menu.themes.THEME_DEFAULT)
    menu.add_button('Play', start_game)
    menu.add_button("Player symbol = {}".format(player_mark), toggle_mark)
    menu.add_button("AI = {}".format(on_off), toggle_cpu)
    menu.add_button("Controls", open_control_menu)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)


windowSize = (800, 800)
windowMarginSides = 30
windowMarginTopAndBottom = 50
window_margin_bottom = 150
gameSize = (windowSize[0] - (2 * windowMarginSides), windowSize[1] - (windowMarginTopAndBottom + window_margin_bottom))
lineSize = 10
backgroundColor = (0, 0, 0)
lineColor = (255, 255, 255)
winColor = (0, 255, 0)
xColor = (200, 0, 0)
oColor = (0, 0, 200)
cpu_player = True
can_play = True
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("TicTacToe")
pygame.font.init()
myFont = pygame.font.SysFont(font, gameSize[0] // 3)
open_main_menu()
