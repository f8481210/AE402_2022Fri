import pygame
import sys
import random
from pygame.locals import *
import quiz as q
import textwrap

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
CYAN  = (  0, 255, 255)
BLINK = [(224,255,255), (192,240,255), (128,224,255), (64,192,255), (128,224,255), (192,240,255)]

# 載入圖片
imgTitle = pygame.image.load("image/title.png")
imgWall = pygame.image.load("image/wall.png")
imgWall2 = pygame.image.load("image/wall2.png")
imgDark = pygame.image.load("image/dark.png")
imgPara = pygame.image.load("image/parameter.png")
imgBtlBG = pygame.image.load("image/btlbg.png")
imgEnemy = pygame.image.load("image/enemy0.png")
imgItem = [
    pygame.image.load("image/pill.png"),
    pygame.image.load("image/potion.png"),
    pygame.image.load("image/spoiled.png"),
    pygame.image.load("image/apple.png"),
    pygame.image.load("image/meat.png")
]
imgFloor = [
    pygame.image.load("image/floor.png"),
    pygame.image.load("image/tbox.png"),
    pygame.image.load("image/cocoon.png"),
    pygame.image.load("image/stairs.png"),
    pygame.image.load("image/blood.png")
]
imgPlayer = [
    pygame.image.load("image/mychr0.png"),
    pygame.image.load("image/mychr1.png"),
    pygame.image.load("image/mychr2.png"),
    pygame.image.load("image/mychr3.png"),
    pygame.image.load("image/mychr4.png"),
    pygame.image.load("image/mychr5.png"),
    pygame.image.load("image/mychr6.png"),
    pygame.image.load("image/mychr7.png"),
    pygame.image.load("image/mychr8.png")
]
imgEffect = [
    pygame.image.load("image/effect_a.png"),
    pygame.image.load("image/effect_b.png")
]

# 宣告變數
speed = 1
idx = 0
tmr = 0
floor = 0
fl_max = 1
welcome = 0

pl_x = 0
pl_y = 0
pl_d = 0
pl_a = 0
pl_lv = 0
pl_lifemax = 0
pl_life = 0
food = 0
treasure = 0

quiz = ''
choice = ''
ans = []
emy_name = ""
emy_lifemax = 0
emy_life = 0
emy_str = 0
emy_x = 0
emy_y = 0
emy_step = 0
emy_blink = 0

dmg_eff = 0
btl_cmd = 0

COMMAND = []
TRE_NAME = ["生命值+20", "生命值+100", "藥物中毒", "飽食度+20", "飽食度+100"]
EMY_NAME = [
    "森林野豬", "哥布林", "獸騎哥布林", "巨獠蜘蛛", "食屍鬼",
    "森之巨狼", "哥布林王", "幽暗騎士", "骷髏法師", "煉獄"
    ]

MAZE_W = 11
MAZE_H = 9
maze = []
for y in range(MAZE_H):
    maze.append([0]*MAZE_W)

DUNGEON_W = MAZE_W*3
DUNGEON_H = MAZE_H*3
dungeon = []
for y in range(DUNGEON_H):
    dungeon.append([0]*DUNGEON_W)

def make_dungeon():
    XP = [ 0, 1, 0,-1]
    YP = [-1, 0, 1, 0]
    #周圍的牆壁
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H-1][x] = 1
    for y in range(1, MAZE_H-1):
        maze[y][0] = 1
        maze[y][MAZE_W-1] = 1

    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            maze[y][x] = 0
    #柱子
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            maze[y][x] = 1
    #從柱子的上下左右延伸出牆壁
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
         d = random.randint(0, 3)
         if x > 2: # 自第二欄的柱子之後，不在左側建立牆壁
             d = random.randint(0, 2)
         maze[y+YP[d]][x+XP[d]] = 1



    for y in range(DUNGEON_H):
        for x in range(DUNGEON_W):
            dungeon[y][x] = 9
    #配置房間與通道
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:
                if random.randint(0, 99) < 20: # 建立房間
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy+ry][dx+rx] = 0
                else: # 建立通道
                    dungeon[dy][dx] = 0
                    if maze[y-1][x] == 0: dungeon[dy-1][dx] = 0
                    if maze[y+1][x] == 0: dungeon[dy+1][dx] = 0
                    if maze[y][x-1] == 0: dungeon[dy][dx-1] = 0
                    if maze[y][x+1] == 0: dungeon[dy][dx+1] = 0

def draw_dungeon(bg, fnt):
    bg.fill(BLACK)
    for y in range(-4, 6):
        for x in range(-5, 6):
            X = (x+5)*80
            Y = (y+4)*80
            dx = pl_x + x
            dy = pl_y + y
            if 0 <= dx and dx < DUNGEON_W and 0 <= dy and dy < DUNGEON_H:
                if dungeon[dy][dx] <= 4:
                    bg.blit(imgFloor[dungeon[dy][dx]], [X, Y])
                if dungeon[dy][dx] == 9:
                    bg.blit(imgWall, [X, Y-40])
                    if dy >= 1 and dungeon[dy-1][dx] == 9:
                        bg.blit(imgWall2, [X, Y-80])
            if x == 0 and y == 0: # 顯示主角
                bg.blit(imgPlayer[pl_a], [X, Y-40])
    bg.blit(imgDark, [0, 0]) # 在四個角落配置暗沉的圖片
    draw_para(bg, fnt) # 顯示主角的能力

def put_event(): # 於地板配置道具
    global pl_x, pl_y, pl_d, pl_a
    # 配置樓梯
    while True:
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if(dungeon[y][x] == 0):
            for ry in range(-1, 2): # 將樓梯周圍的空間設定為地板
                for rx in range(-1, 2):
                    dungeon[y+ry][x+rx] = 0
            dungeon[y][x] = 3
            break
    # 配置寶箱、繭與帶血地板
    for i in range(60):
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if(dungeon[y][x] == 0):
            dungeon[y][x] = random.choice([1,2,2,2,2,2,4,4,4,4,4])

    # 玩家的初始位置
    while True:
        pl_x = random.randint(3, DUNGEON_W-4)
        pl_y = random.randint(3, DUNGEON_H-4)
        if(dungeon[pl_y][pl_x] == 0):
            break
    pl_d = 1
    pl_a = 2
                
def move_player(key): # 主角的移動
    global idx, tmr, pl_x, pl_y, pl_d, pl_a, pl_life, food, treasure, pl_lifemax

    if dungeon[pl_y][pl_x] == 1: # 走到寶箱的位置
        dungeon[pl_y][pl_x] = 0
        treasure = random.choice([0,0,0,0,0,0,1,1,1,2])
        if treasure == 0:
            pl_life += 20
            if pl_life > pl_lifemax:
                pl_life = pl_lifemax
        if treasure == 1:
            pl_life += 100
            if pl_life > pl_lifemax:
                pl_life = pl_lifemax
        if treasure == 2:
            food -= 70
        idx = 3
        tmr = 0
        return
    if dungeon[pl_y][pl_x] == 2: # 走到繭的位置
        dungeon[pl_y][pl_x] = 0
        r = random.randint(0, 99)
        if r < 40: # 食物
            treasure = random.choice([3,3,3,4])
            if treasure == 3: food = food + 20
            if treasure == 4: food = food + 100
            idx = 3
            tmr = 0
        else: # 敵人出現
            idx = 10
            tmr = 0
        return
    if dungeon[pl_y][pl_x] == 3: # 走到樓梯的位置
        idx = 2
        tmr = 0
        return

    # 以方向鍵上下左右移動
    x = pl_x
    y = pl_y
    if key[K_UP] == 1:
        pl_d = 0
        if dungeon[pl_y-1][pl_x] != 9:
            pl_y = pl_y - 1
    if key[K_DOWN] == 1:
        pl_d = 1
        if dungeon[pl_y+1][pl_x] != 9:
            pl_y = pl_y + 1
    if key[K_LEFT] == 1:
        pl_d = 2
        if dungeon[pl_y][pl_x-1] != 9:
            pl_x = pl_x - 1
    if key[K_RIGHT] == 1:
        pl_d = 3
        if dungeon[pl_y][pl_x+1] != 9:
            pl_x = pl_x + 1
    pl_a = pl_d*2
    if pl_x != x or pl_y != y: # 移動時，計算食物的存量與體力
        pl_a = pl_a + tmr%2 # 移動時的原地踏步動畫
        if food > 0:
            food = food - 1
        else:
            pl_life = pl_life - 5
            if pl_life <= 0:
                pl_life = 0
                pygame.mixer.music.stop()
                idx = 9
                tmr = 0

def draw_text(bg, txt, pos, fnt, col): # 顯示套用陰影效果的文字
    x, y = pos
    words = [word.split(' ') for word in txt.splitlines()]  # 2D array where each row is a list of words.
    space = fnt.size(' ')[0]  # The width of a space.
    max_width, max_height = bg.get_size()
    for line in words:
        for word in line:
            word_bg1 = fnt.render(word, True, BLACK)
            word_bg2 = fnt.render(word, True, col)
            word_width, word_height = word_bg1.get_size()
            word_width, word_height = word_bg2.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            bg.blit(word_bg1, (x+1, y+2))
            bg.blit(word_bg2, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def draw_para(bg, fnt): # 顯示主角的能力
    X = 30
    Y = 600
    bg.blit(imgPara, [X, Y])
    col = WHITE
    if pl_life < 10 and tmr%2 == 0: col = RED
    draw_text(bg, "{}/{}".format(pl_life, pl_lifemax), (X+128, Y+3), fnt, col)
    draw_text(bg, str(pl_lv), (X+128, Y+30), fnt, WHITE)
    col = WHITE
    if food == 0 and tmr%2 == 0: col = RED
    draw_text(bg, str(food), (X+128, Y+57), fnt, col)

def init_battle(): # 準備進入戰鬥
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, quiz
    q.get_quiz()
    quiz = q.quiz
    typ = random.randint(0, floor)
    if floor >= 10:
        typ = random.randint(0, 9)
    lev = random.randint(1, floor)
    imgEnemy = pygame.image.load("image/enemy"+str(typ)+".png")
    emy_name = EMY_NAME[typ] + " 等級" + str(lev)
    emy_lifemax = 80*(typ+1) + (lev-1)*10
    emy_life = emy_lifemax
    emy_str = int(emy_lifemax/3)
    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()

    

def draw_bar(bg, x, y, w, h, val, max): # 敵人體力條
    pygame.draw.rect(bg, WHITE, [x-2, y-2, w+4, h+4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, (0,128,255), [x, y, w*val/max, h])

def draw_battle(bg, fnt): # 繪製戰鬥畫面
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff = dmg_eff - 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [bx, by])
    if emy_life > 0 and emy_blink%2 == 0:
        bg.blit(imgEnemy, [emy_x, emy_y+emy_step])
    draw_bar(bg, 340, 580, 200, 10, emy_life, emy_lifemax)
    if emy_blink > 0:
        emy_blink = emy_blink - 1
    for i in range(5): # 顯示戰鬥訊息
        draw_text(bg, message[i], (650, 360+i*40), fnt, WHITE)
    draw_para(bg, fnt) # 顯示主角能力

def battle_command(bg, fnt, key): # 輸入與顯示指令
    global btl_cmd
    ent = False
    if key[K_a]: # A鍵
        btl_cmd = 0
        ent = True
    if key[K_b]: # B鍵
        btl_cmd = 1
        ent = True
    if key[K_c]: # C鍵
        btl_cmd = 2
        ent = True
    if key[K_d]: # D鍵
        btl_cmd = 3
        ent = True
    if key[K_UP] and btl_cmd > 0: #↑鍵
        btl_cmd -= 1
    if key[K_DOWN] and btl_cmd < 3: #↓鍵
        btl_cmd += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(4):
        c = WHITE
        if btl_cmd == i: c = BLINK[tmr%6]
        COMMAND = q.choice
        draw_text(bg, COMMAND[i], (20, 360+i*60), fnt, c)
    return ent

# 顯示戰鬥訊息的處理
message = [""]*5
def init_message():
    for i in range(5):
        message[i] = ""
    
def set_message(msg):
    for i in range(5):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(4):
        message[i] = message[i+1]
    message[4] = msg

def wrap(string, max_width):
    return textwrap.fill(string,max_width)

def main(): # 主要處理
    global speed, idx, tmr, floor, fl_max, welcome
    global pl_a, pl_lv, pl_lifemax, pl_life, food
    global emy_life, emy_step, emy_blink, dmg_eff
    dmg = 0
    lif_p = 0
    str_p = 0

    pygame.init()
    pygame.display.set_caption("死亡森林")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font("font/TaipeiSansTCBeta-Regular.ttf", 30)
    fontS = pygame.font.Font("font/TaipeiSansTCBeta-Regular.ttf", 20)

    se = [ # 音效
        pygame.mixer.Sound("sound/ohd_se_attack.ogg"),
        pygame.mixer.Sound("sound/ohd_se_blaze.ogg"),
        pygame.mixer.Sound("sound/ohd_se_potion.ogg"),
        pygame.mixer.Sound("sound/ohd_jin_gameover.ogg"),
        pygame.mixer.Sound("sound/ohd_jin_levup.ogg"),
        pygame.mixer.Sound("sound/ohd_jin_win.ogg")
    ]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    speed = speed + 1
                    if speed == 4:
                        speed = 1

        tmr = tmr + 1
        key = pygame.key.get_pressed()

        if idx == 0: # 標題畫面
            if tmr == 1:
                pygame.mixer.music.load("sound/ohd_bgm_title.ogg")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            screen.blit(imgTitle, [0, 0])
            if fl_max >= 2:
                draw_text(screen, "你抵達死亡森林{}".format(fl_max), (300, 460), font, CYAN)
            draw_text(screen, "按下空白鍵", (360, 560), font, BLINK[tmr%6])
            if key[K_SPACE] == 1:
                make_dungeon()
                put_event()
                floor = 1
                welcome = 15
                pl_lifemax = 300
                pl_life = pl_lifemax
                pl_lv = 1
                food = 300
                idx = 1
                pygame.mixer.music.load("sound/ohd_bgm_field.ogg")
                pygame.mixer.music.play(-1)

        elif idx == 1: # 玩家的移動
            move_player(key)
            draw_dungeon(screen, fontS)
            draw_text(screen, "floor {} ({},{})".format(floor, pl_x, pl_y), (60, 40), fontS, WHITE)
            if welcome > 0:
                welcome = welcome - 1
                draw_text(screen, "歡迎來到死亡森林{}".format(floor), (300, 180), font, CYAN)

        elif idx == 2: # 切換畫面
            draw_dungeon(screen, fontS)
            if 1 <= tmr and tmr <= 5:
                h = 80*tmr
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            if tmr == 5:
                floor = floor + 1
                if floor > fl_max:
                    fl_max = floor
                welcome = 15
                make_dungeon()
                put_event()
            if 6 <= tmr and tmr <= 9:
                h = 80*(10-tmr)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            if tmr == 10:
                idx = 1

        elif idx == 3: # 取得道具或踩到陷阱
            draw_dungeon(screen, fontS)
            screen.blit(imgItem[treasure], [320, 220])
            draw_text(screen, TRE_NAME[treasure], (380, 240), font, WHITE)
            if tmr == 10:
                idx = 1

        elif idx == 9: # 遊戲結束
            if tmr <= 30:
                PL_TURN = [2, 4, 0, 6]
                pl_a = PL_TURN[tmr%4]
                if tmr == 30: pl_a = 8 # 主角倒地的畫面
                draw_dungeon(screen, fontS)
            elif tmr == 31:
                se[3].play()
                draw_text(screen, "你身亡了...", (360, 240), font, RED)
                draw_text(screen, "遊戲結束", (360, 380), font, RED)
            elif tmr == 100:
                idx = 0
                tmr = 0

        elif idx == 10: # 開始戰鬥
            if tmr == 1:
                pygame.mixer.music.load("sound/ohd_bgm_battle.ogg")
                pygame.mixer.music.play(-1)
                init_battle()
                init_message()
            elif tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(imgBtlBG, [bx, by])
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name+" 出現!", (300, 200), font, WHITE)
            else:
                idx = 11
                tmr = 0

        elif idx == 11: # 輪到玩家攻擊（等待指令輸入）
            global quiz
            draw_battle(screen, fontS)
            font = pygame.font.Font("font/TaipeiSansTCBeta-Regular.ttf", 30)    
            draw_text(screen, wrap(quiz,25), (20, 100), font, WHITE)
            ans = q.ans
            if tmr == 1:
                set_message("請作答!")
            if battle_command(screen, font, key) == True:
                if btl_cmd == ans:
                    idx = 12
                    tmr = 0
                else:
                    idx = 13
                    tmr = 0


        elif idx == 12: # 玩家發動攻擊
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("正確答案!")
                se[0].play()
                dmg = emy_life
            if 2 <= tmr and tmr <= 4:
                screen.blit(imgEffect[0], [700-tmr*120, -100+tmr*120])
            if tmr == 5:
                emy_blink = 5
            if tmr == 11:
                emy_life = emy_life - dmg
                if emy_life <= 0:
                    emy_life = 0
                    idx = 16
                    tmr = 0
            if tmr == 16:
                idx = 13
                tmr = 0

        elif idx == 13: # 輪到敵人攻擊
            draw_battle(screen, fontS)
            if tmr == 5:
                set_message("錯誤答案!")
                se[0].play()
                emy_step = 30
            if tmr == 9:
                dmg = emy_str + random.randint(0, 20)
                set_message('造成'+str(dmg)+"點傷害!")
                dmg_eff = 5
                emy_step = 0
            if tmr == 15:
                pl_life = pl_life - dmg
                if pl_life < 0:
                    pl_life = 0
                    idx = 15
                    tmr = 0
            if tmr == 20:
                idx = 11
                tmr = 0
             
        elif idx == 15: # 失敗
            draw_battle(screen, fontS)
            if tmr == 1:
                pygame.mixer.music.stop()
                set_message("失敗...")
            if tmr == 11:
                idx = 9
                tmr = 29

        elif idx == 16: # 勝利
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("勝利!")
                pygame.mixer.music.stop()
                se[5].play()
            if tmr == 28:
                idx = 22
                if random.randint(0, emy_lifemax) > random.randint(0, pl_lifemax):
                    idx = 17
                    tmr = 0

        elif idx == 17: # 升級
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("等級提升!")
                pl_lv += 1
                se[4].play()
                lif_p = random.randint(10, 20)
            if tmr == 21:
                set_message("生命值上限 + "+str(lif_p))
                pl_lifemax = pl_lifemax + lif_p
            if tmr == 50:
                idx = 22


        elif idx == 22: # 戰鬥結束
            pygame.mixer.music.load("sound/ohd_bgm_field.ogg")
            pygame.mixer.music.play(-1)
            idx = 1

        draw_text(screen, "[S]速度 "+str(speed), (740, 40), fontS, WHITE)

        pygame.display.update()
        clock.tick(4+2*speed)

if __name__ == '__main__':
    main()
