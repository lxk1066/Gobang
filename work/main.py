# a mini-game for gobang(five-in-a-row)
# -*- coding:UTF-8 -*-
import tkinter.messagebox
import pygame
import time
import math
from tkinter import *
from tkinter.messagebox import *
from Class import Player
Tk().wm_withdraw()


# 判断先后手
def judge_sequence():
    if play_black.get_initiative():
        return 1
    elif play_white.get_initiative():
        return 2


# 判断是否平局
# 遍历数组，如果发现-1就说明棋盘上还有空位没下棋子
def judge_dogfall():
    for i in board:
        for j in i:
            if j == -1:
                return False
    return True


# 判断谁是winner
def judge_winner():
    if play_black.get_status():
        return "player_black"
    elif play_white.get_status():
        return "player_white"


# 判断谁是loser
def judge_loser():
    if play_black.get_status() is None:
        return None
    if not play_black.get_status():
        return "player_black"
    elif not play_white.get_status():
        return "player_white"


# 保存对局记录
def save_result():
    localtime = time.asctime(time.localtime(time.time()))
    with open('save_result.txt', 'a+', encoding='utf-8') as f:
        f.write("{}\n".format(localtime))
        f.write("胜方: {}\n负方: {}\n".format(judge_winner(), judge_loser()))
        f.write("对局棋谱: \n")
        for i in board:
            for j in i:
                if j == -1:
                    f.write("■\t")
                elif j == 1:
                    f.write("黑\t")
                else:
                    f.write("白\t")
            f.write("\n")
        f.write("\n")


# 根据鼠标所在位置坐标返回格子坐标
def position(mouse_post):
    p = 0
    post = [0, 0]
    for i in mouse_post:
        position_x = math.fabs(i % 50)
        position_y = int(i / 50)
        if position_x >= 50 - r:
            position_y += 1
        elif position_x <= r:
            pass
        else:
            return False
        post[p] = position_y
        p += 1
    return post


# 根据position()返回值计算出在二维数组board中的对应位置并判断是否可以下(棋)子
def judge_board(mouse_now, *args):
    position_num = position(mouse_now)
    if not position_num:
        return False
    a = position_num[1] - 1
    b = position_num[0] - 1
    if len(args) != 0:
        board[a][b] = args[0]
    return True if board[a][b] == -1 else False


# 返回点击区域的顶点坐标, 触发半径为15px
def getx_gety(mouse_post):
    num = position(mouse_post)

    return [num[0] * 50, num[1] * 50]


# 算出画圆的圆心坐标，参数post_circle来自getx_gety()函数的返回值
# 在正方形内画圆，圆心坐标计算公式为((x1+x2+x3+x4)/4,(y1+y2+y3+y4)/4)
def circle_post(post_circle):
    post_x, post_y = 0, 0
    for q in post_circle:
        post_x += q[0]
        post_y += q[1]
    pos = [post_x / 4, post_y / 4]
    return pos


# ----------------------------------------逻辑部分------------------------------------------------
# 判断结果
def compute():
    i = 0
    result = -1
    # 检查行
    while (result == -1) and (i < wide):
        num_of_black, num_of_white = 0, 0
        j = 0
        while j < wide:
            if board[i][j] == 1:
                if j > 0:
                    if board[i][j-1] == 0 or board[i][j-1] == -1:
                        num_of_black = 0
                num_of_black += 1
            elif board[i][j] == 0:
                if j > 0:
                    if board[i][j-1] == 1 or board[i][j-1] == -1:
                        num_of_white = 0
                num_of_white += 1
            if num_of_white == size:
                result = 0
            elif num_of_black == size:
                result = 1
            j += 1
        i += 1
    # 检查列
    if result == -1:
        i, j = 0, 0
        while j < wide and result == -1:
            num_of_black = num_of_white = 0
            i = 0
            while i < wide:
                if board[i][j] == 1:
                    if i > 0:
                        if board[i-1][j] == 0 or board[i-1][j] == -1:
                            num_of_black = 0
                    num_of_black += 1
                elif board[i][j] == 0:
                    if i > 0:
                        if board[i-1][j] == 1 or board[i-1][j] == -1:
                            num_of_white = 0
                    num_of_white += 1
                if num_of_white == size:
                    result = 0
                elif num_of_black == size:
                    result = 1
                i += 1
            j += 1
    # 检查正对角线
    if result == -1:
        out_i, out_j = wide - 5, 0
        while out_i >= 0:
            num_of_white = num_of_black = 0
            i, j = out_i, out_j
            while j < wide and i < wide:
                if board[j][i] == 1:
                    if i > 0:
                        if board[j-1][i-1] == 0 or board[j-1][i-1] == -1:
                            num_of_black = 0
                    num_of_black += 1
                elif board[j][i] == 0:
                    if i > 0:
                        if board[j-1][i-1] == 1 or board[j-1][i-1] == -1:
                            num_of_white = 0
                    num_of_white += 1
                if num_of_white == size:
                    result = 0
                    return result
                elif num_of_black == size:
                    result = 1
                    return result
                i += 1
                j += 1
            out_i -= 1
        out_i, out_j = 0, wide - 5
        while out_j > 0:
            num_of_white = num_of_black = 0
            i, j = out_i, out_j
            while j < wide and i < wide:
                if board[j][i] == 1:
                    if j > 0:
                        if board[j-1][i-1] == 0 or board[j-1][i-1] == -1:
                            num_of_black = 0
                    num_of_black += 1
                elif board[j][i] == 0:
                    if j > 0:
                        if board[j-1][i-1] == 1 or board[j-1][i-1] == -1:
                            num_of_white = 0
                    num_of_white += 1
                if num_of_white == size:
                    result = 0
                    return result
                elif num_of_black == size:
                    result = 1
                    return result
                i += 1
                j += 1
            out_j -= 1

    # 检查斜对角线
    if result == -1:
        out_i, out_j = 4, 0
        while out_i <= 9:
            num_of_white = num_of_black = 0
            i, j = out_i, out_j
            while i >= 0:
                if board[i][j] == 1:
                    if j > 0:
                        if board[i+1][j-1] == 0 or board[i+1][j-1] == -1:
                            num_of_black = 0
                    num_of_black += 1
                elif board[i][j] == 0:
                    if j > 0:
                        if board[i+1][j-1] == 1 or board[i+1][j-1] == -1:
                            num_of_white = 0
                    num_of_white += 1
                if num_of_white == size:
                    result = 0
                    return result
                elif num_of_black == size:
                    result = 1
                    return result
                i -= 1
                j += 1
            out_i += 1
        out_i, out_j = 9, 5
        while out_j > 0:
            num_of_white = num_of_black = 0
            i, j = out_i, out_j
            while j < wide:
                if board[i][j] == 1:
                    if i < 9:
                        if board[i+1][j-1] == 0 or board[i+1][j-1] == -1:
                            num_of_black = 0
                    num_of_black += 1
                elif board[i][j] == 0:
                    if i < 9:
                        if board[i+1][j-1] == 1 or board[i+1][j-1] == -1:
                            num_of_white = 0
                    num_of_white += 1
                if num_of_white == size:
                    result = 0
                    return result
                elif num_of_black == size:
                    result = 1
                    return result
                i -= 1
                j += 1
            out_j -= 1
    return result


# ---------------------------------------GUI图形部分------------------------------------------
# 画图
def paint_circle(mouse_now):
    if judge_sequence() == 1:
        color = black
    else:
        color = white
    post = getx_gety(mouse_now)
    pygame.draw.circle(screen, color, post, 20, 0)


# 提示先后手的那两个圆
def paint_circle_first():
    pygame.draw.circle(screen, black, [625, 60], 20, 0)


def paint_circle_next():
    pygame.draw.circle(screen, black, [625, 145], 20, 0)


def paint_game_restart():
    pygame.draw.rect(screen, black, [100, 540, 100, 30], 5)
    screen.blit(game_restart_text, (110, 545))


# 刷新背景
def background():
    screen.fill([87, 166, 230])
    a, b = 50, 50
    p, m = 0, 0
    image = pygame.image.load(r"./background.jpg")
    screen.blit(image, (0, 0))

    for i in range(9):
        for j in range(9):
            pygame.draw.rect(screen, black, [a + 50 * p, a, b, b + 50 * m], 1)
            p += 1
        p = 0
        m += 1

    paint_game_restart()
    pygame.display.update()


if __name__ == "__main__":
    while True:
        # 主程序
        size = 5
        wide = 10
        n = 0        # 判断游戏是否结束的全局变量
        r = 20       # 下子时鼠标点击的触发半径，单位px
        board = []
        white = [255, 255, 255]
        black = [0, 0, 0]
        bright_green = (0, 255, 0)
        lightgrey = [125, 125, 125]
        my_blue = [199, 193, 245]

        for k in range(wide):
            board.append([])
            for h in range(wide):
                board[k].append(-1)

        pygame.init()
        pygame.display.init()
        screen = pygame.display.set_mode([550, 600])
        pygame.display.set_caption("tic_tac_toe")
        my_font = pygame.font.Font("fzlt.ttf", 20)
        game_restart_text = my_font.render("重新开始", True, black)
        # 刷新背景
        background()

        # 让用户选择是O为先手还是X为先手
        if tkinter.messagebox.askyesno("提示", "请选择先手是画O(Y)或者画X(N)？\n      其中O为左击，X为右击"):
            initiative = 1
        else:
            initiative = 0

        if initiative:
            play_black = Player(True)
            play_white = Player(False)
        else:
            play_black = Player(False)
            play_white = Player(True)

        while True:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                print(mouse[0], mouse[1])

                # # 通过判断先后手来更新右上角的提示
                # if judge_sequence() == 1 and n == 0:
                #     paint_circle_first()
                #     pygame.draw.circle(screen, [199, 193, 245], [625, 145], 17, 0)
                # elif judge_sequence() == 2 and n == 0:
                #     paint_circle_next()
                #     pygame.draw.circle(screen, [199, 193, 245], [625, 60], 17, 0)
                # pygame.display.update()

                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 鼠标的x坐标
                    x = event.pos[0]
                    # 鼠标的y坐标
                    y = event.pos[1]

                    # 点击重新开始按钮
                    if 100 < mouse[0] < 200 and 540 <= mouse[1] <= 570 and event.button == 1:
                        n = 1

                    # 通过鼠标坐标和其他条件来判断下(棋)子
                    if n == 0:
                        if (50 - r) < mouse[0] < (500 + r) and (50 - r) < mouse[1] < (500 + r):
                            if judge_board(mouse):
                                if event.button == 1 and judge_sequence() == 1:
                                    paint_circle(mouse)
                                    judge_board(mouse, 1)
                                    pygame.display.update()
                                    play_black.update()
                                    play_white.update()
                                elif event.button == 3 and judge_sequence() == 2:
                                    paint_circle(mouse)
                                    judge_board(mouse, 0)
                                    pygame.display.update()
                                    play_black.update()
                                    play_white.update()

                    if n == 0:
                        if compute() == 1:
                            showinfo("提示", "黑 WIN!")
                            play_black.set_winner()
                            play_white.set_loser()
                            n = 2
                        elif compute() == 0:
                            showinfo("提示", "白 WIN!")
                            play_white.set_winner()
                            play_black.set_loser()
                            n = 2
                        elif judge_dogfall() and compute() == -1:
                            showinfo("提示", "平局！")
                            n = 2

                    if n == 2:
                        # paint_game_records()
                        save_result()

            # 重新开始
            if n == 1:
                break
