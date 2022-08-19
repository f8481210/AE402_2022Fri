#!/usr/bin/python3.7
# Please note that this project is meant to run in Pygame 2.
# Setup Python ----------------------------------------------- #
import pygame, sys, random, math
import data.entities as e
import data.lines as line_math
import data.text as text
from data.core_funcs import *

BORDER_WIDTH = 70

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)
pygame.display.set_caption('Lynez')
screen = pygame.display.set_mode((550 + 2 * BORDER_WIDTH, 800),0,32) # 螢幕大小

display = pygame.Surface((275, 400))
gui_display = pygame.Surface((275, 400))
gui_display.set_colorkey((0, 0, 0))

e.load_particle_images('data/images/particles') # 載入粒子圖檔
e.set_global_colorkey((0, 0, 0)) # 更新colorkey (背景顏色)

font = text.Font('data/fonts/large_font.png', (255, 255, 255))  # 建立白色字體
font2 = text.Font('data/fonts/large_font.png', (0, 0, 1))       # 建立黑色字體

# 匯進音檔
bounce_s = pygame.mixer.Sound('data/sfx/bounce.wav')
death_s = pygame.mixer.Sound('data/sfx/death.wav')
laser_charge_s = pygame.mixer.Sound('data/sfx/laser_charge.wav')
laser_explode_s = pygame.mixer.Sound('data/sfx/laser_explode.wav')
place_s = pygame.mixer.Sound('data/sfx/place.wav') # 從data/sfx讀取place.wav音檔
restart_s = pygame.mixer.Sound('data/sfx/restart.wav')

# 變更音量
bounce_s.set_volume(0.3)
place_s.set_volume(0.3) # 設定place_s的音量
laser_charge_s.set_volume(0.05)

# 初始設定
particles = []
platforms = [[[0, display.get_height() - 1], [display.get_width(), display.get_height() - 1]]]
last_point = [display.get_width() // 2, display.get_height()]
scroll = 0
square_effects = []

background_color = (13, 20, 33)
background_polygon_color = (24, 34, 46)
line_color = (255, 255, 255)
line_placing_color = (90, 140, 170)
line_width = 3

player_pos = [display.get_width() // 2, display.get_height() // 2]
player_velocity = [0, 0]
player_color = (90, 210, 255)
player_gravity = 0.05
player_terminal_velocity = 1
bounce_strength = 1
bounce_cooldown = 0

# 檢查 point在線的上方or下方
def check_line_sides(lines, point): # OK
    line_status = []
    for line in lines:
        line_status.append((line[1][0] - line[0][0]) * (point[1] - line[0][1]) - (line[1][1] - line[0][1]) * (point[0] - line[0][0]))
    return line_status

# 回傳 1 或是 -1
def sign(num): # OK
    if num != 0:
        return num / abs(num)
    else:
        return 1

# 計算反射的角度
def mirror_angle(original,base): # OK
    dif = 180-base
    base = 180
    new = original+dif
    new = new % 360
    dif = base-new
    return original + dif * 2

def dis_func(dis):
    return math.sqrt(dis[0] ** 2 + dis[1] ** 2)

lasers = []
line_effects = []
sparks = []
circle_effects = []

player_path = []
game_score = 0

end_game = False
game_text_loc = - 120
end_text_loc = -220

last_place = 50

screen_shake = 0

transition = 30

pygame.mixer.music.load('data/music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    if transition > 0:
        transition -= 1

    if screen_shake > 0:
        screen_shake -= 1

    if not end_game: # 計算屏幕的轉動(往上移動)
        line_color = (255, 255, 255) # 固定在螢幕上的白線
        if player_pos[1] - 200 < scroll:
            scroll += (player_pos[1] - 200 - scroll) / 10
    else:
        line_color = (190, 197, 208) # 隨著鼠標移動的藍線


    # 隨機生成實線，增加遊戲難度
    if (-scroll) - last_place > 50:
        if random.randint(1, 3) <= 2:
            base_y = scroll - 80 # 高度固定
            base_x = random.randint(0, display.get_width()) # 左右位置隨機生成
            # 隨機生成 線的長度、傾斜角度
            new_line = [[base_x, base_y], [base_x + random.randint(0, 200) - 100, base_y + random.randint(0, 100) - 50]]

            # 傾斜角大於30度，才append到list中
            if dis_func((new_line[1][0] - new_line[0][0], new_line[1][1] - new_line[0][1])) > 30:
                new_line.sort() 
                platforms.append(new_line)
        last_place += 50 

    # 計算遊戲分數
    game_score = max(game_score, -(player_pos[1] - display.get_height() // 2))

    # 遊戲背景顏色
    display.fill((background_color))
    gui_display.fill((0,0,0))

    mx, my = pygame.mouse.get_pos()
    mx -= BORDER_WIDTH
    mx = mx // 2
    my = my // 2

    player_gravity = 0.05 + game_score / 30000
    player_terminal_velocity = 1 + game_score / 3000
    bounce_strength = 1 + game_score / 8000     # 更新彈跳的力度

    # 當遊戲結束時，背景往下掉
    if end_game:
        scroll += (- scroll) / 100

    # 背景的方塊 ----------------------------------------- #
    # square_effects[0] : 位置
    # square_effects[1] : 旋轉角度
    # square_effects[2] : 旋轉速度
    # square_effects[3] : 方塊大小
    # square_effects[4] : 下降速度
    if random.randint(1, 60) == 1:
        square_effects.append([[random.randint(0, display.get_width()), -80 + scroll], random.randint(0, 359), random.randint(10, 30) / 20, random.randint(15, 40), random.randint(10, 30) / 500])

    for i, effect in sorted(enumerate(square_effects), reverse=True): # loc, rot, speed, size, decay
        effect[0][1] += effect[2]
        effect[1] += effect[2] * effect[4]
        effect[3] -= effect[4]  

        # 計算方形的四個點
        points = [
            advance(effect[0], math.degrees(effect[1]), effect[3]),
            advance(effect[0], math.degrees(effect[1]) + 90, effect[3]),
            advance(effect[0], math.degrees(effect[1]) + 180, effect[3]),
            advance(effect[0], math.degrees(effect[1]) + 270, effect[3]),
        ]
        points = [[v[0], v[1] - scroll] for v in points]

        if effect[3] < 1: # 當方塊太小，從list中移除
            square_effects.pop(i)
        else: # 根據4個點匯出方形
            pygame.draw.polygon(display, background_polygon_color, points, 2)

    # 線條效果 ------------------------------------------- #
    # effect[0] ： 初始位置
    # effect[1] ： 結束位置
    # effect[2] ： 顏色
    # effect[3] ： 繪製的速度
    # effect[4] ： 線的生命值(小於0，pop) 
    for i, effect in sorted(enumerate(line_effects), reverse=True): # locs, targets, color, speed, dur
        if len(effect) == 5:
            effect.append(effect[4])
        effect[0][0][0] += (effect[1][0][0] - effect[0][0][0]) / effect[3]
        effect[0][0][1] += (effect[1][0][1] - effect[0][0][1]) / effect[3]
        effect[0][1][0] += (effect[1][1][0] - effect[0][1][0]) / effect[3]
        effect[0][1][1] += (effect[1][1][1] - effect[0][1][1]) / effect[3]
        
        effect[4] -= 1      # 減少線的生命
        if effect[4] <= 0:  # 生命少於0，pop出list
            line_effects.pop(i)

        opacity = 255 * (effect[4] / effect[5]) # 計算透明值
        color = (effect[2][0], effect[2][1], effect[2][2], opacity) # color = (r,g,b,透明值)
        
        # 繪出線條於螢幕上
        alpha_line(display, color, effect[0][0], effect[0][1])

    # 繪製圓圈的事件 ----------------------------------------- #
    # circle[0] ： 位置
    # circle[1] ： 半徑
    # circle[2] ： 邊線的粗細
    # circle[3] ： 圓圈變大的速度
    # circle[4] ： 顏色
    for i, circle in sorted(enumerate(circle_effects), reverse=True): # loc, radius, border_stats, speed_stats, color
        circle[1] += circle[3][0]
        circle[2][0] -= circle[2][1]
        circle[3][0] -= circle[3][1]

        # 當邊界粗細過小，則pop該圓圈
        if circle[2][0] < 1:
            circle_effects.pop(i)
        else: # 依據條件繪製圓圈
            pygame.draw.circle(display, circle[4], [int(circle[0][0]), int(circle[0][1] - scroll)], int(circle[1]), int(circle[2][0]))

    # 火花 ------------------------------------------------- #
    # spark[0] ： 位置
    # spark[1] ： 方向(角度)
    # spark[2] ： 長度
    # spark[3] ： 速度
    for i, spark in sorted(enumerate(sparks), reverse=True): # loc, dir, scale, speed
        speed = spark[3]
        scale = spark[2]

        # 計算火花
        points = [
            advance(spark[0], spark[1], 2 * speed * scale),
            advance(spark[0], spark[1] + 90, 0.3 * speed * scale),
            advance(spark[0], spark[1], -1 * speed * scale),
            advance(spark[0], spark[1] - 90, 0.3 * speed * scale),
        ]
        points = [[v[0], v[1] - scroll] for v in points]
        color = (255, 255, 255)

        # 如果spark的參數超過4個，代表第四個元素是顏色
        if len(spark) > 4:
            color = spark[4]

        pygame.draw.polygon(display, color, points) # 根據座標匯出多邊形

        spark[0] = advance(spark[0], spark[1], speed) # 根據角度更新位置，等待下次的繪製
        spark[3] -= 0.5
        if spark[3] <= 0:
            sparks.pop(i)

    # 將線條繪至於螢幕上  ------------------------------------ #
    # 線條的一端是最後一個圓圈的位置，另外一端為鼠標位置
    if not end_game:
        pygame.draw.line(display, line_placing_color, [last_point[0], last_point[1] - scroll], [mx, my])

    # 取player_path的最後50個元素
    player_path = player_path[-50:]

    # 如果取出來的個數大於2個
    if len(player_path) > 2: 
        player_path_mod = [[v[0], v[1] - scroll] for v in player_path] # 計算出實線下的陰影
        pygame.draw.lines(display, line_placing_color, False, player_path_mod) # 匯出實線下的陰影

    # 雷射線條 ------------------------------------------------- #
    if game_score > 300: # 超過300分時，隨機生成雷射，增加遊戲難度
        if random.randint(1, 300 * (1 + len(lasers) * 2)) == 1:
            lasers.append([random.randint(0, display.get_width()), random.randint(90, 150), 20])


    for i, laser in sorted(enumerate(lasers), reverse=True):

        # 計算出雷射段的最左邊
        left = laser[0] - laser[1] // 2
        if left < 0:
            left = 0

        # 計算出雷射段的最右邊
        right = laser[0] + laser[1] // 2
        if right > display.get_width():
            right = display.get_width()

        # 繪出最左與最右的紅色垂直線   
        pygame.draw.line(display, (190, 40, 100), (left, 0), (left, display.get_height()))
        pygame.draw.line(display, (190, 40, 100), (right, 0), (right, display.get_height()))

        center_line = [[laser[0], 0], [laser[0], display.get_height()]]
        if laser[2] % 12 == 0:
            laser_charge_s.play()

            # 行程由雷射左右兩邊 往中間滑動的紅色直線
            line_effects.append([[[left, 0], [left, display.get_height()]], center_line, (190, 40, 100), 20, 30])
            line_effects.append([[[right, 0], [right, display.get_height()]], center_line, (190, 40, 100), 20, 30])

        # 控制雷射的生命
        laser[2] += 1

        # 若雷射生命大於180，則pop出list
        if laser[2] > 180:
            lasers.pop(i)
            laser_explode_s.play()

            # 當粒子在雷射的距離之間
            if (player_pos[0] > left) and (player_pos[0] < right):


                if player_pos[0] > laser[0]: # 若粒子在雷射的右半部
                    player_velocity[0] += 4  # 更改粒子的運動方向
                else:                        # 若粒子在雷射的左半部
                    player_velocity[0] -= 4  # 更改粒子的運動方向

                # 繪製出撞擊到的灰色射線以及灰色粒子
                #　可以參考這個網址的圖片，https://pythonprogramming.altervista.org/lynez-new-great-game-from-dafluffypotato/
                for i in range(30):
                    # 建立撞擊到的射線
                    sparks.append([player_pos, random.randint(0, 359), random.randint(7, 10) / 10 * 3, 9 * random.randint(5, 10) / 10, (170, 170, 170)])

                    # 建粒灰色的粒子
                    # 隨機生成粒子位置的旋轉角度
                    a = random.randint(0, 359)
                    s = random.randint(20, 50) / 10
                    x_p = math.cos(math.radians(a)) * s
                    y_p = math.sin(math.radians(a)) * s

                    # 根據player_pos加上偏差角度 生成灰色粒子物件
                    particles.append(e.particle(player_pos, 'p', [x_p, y_p], 0.1, random.randint(0, 20) / 10, (170, 170, 170)))
                    screen_shake = 8

            # 繪製雷射消失時的畫面效果
            for i in range(300):

                # 計算粒子的運動方向
                if random.randint(1, 2) == 1:
                    pos_x = left
                    vel = [4 + random.randint(0, 20) / 10, random.randint(0, 10) / 10 - 3]
                else:
                    pos_x = right
                    vel = [-(4 + random.randint(0, 20) / 10), random.randint(0, 10) / 10 - 3]

                # 隨機生成粒子的高度
                pos_y = random.randint(0, display.get_height() + 30) + scroll - 30
                # 創建一個新的粒子，並append 到 particles中
                particles.append(e.particle([pos_x, pos_y], 'p', vel, 0.2, random.randint(0, 20) / 10, (160, 40, 80)))

    # Render Platforms --------------------------------------- #
    # 繪製反彈的平台 --------------------------------------- #
    for platform in platforms:
        if (min(platform[0][1], platform[1][1]) < scroll + display.get_height() + 20) and (max(platform[0][1], platform[1][1]) > scroll - 20):
            # 繪製白色實線
            pygame.draw.line(display, line_color, [platform[0][0], platform[0][1] - scroll], [platform[1][0], platform[1][1] - scroll], line_width)
            # 線左右兩邊的圓形
            pygame.draw.circle(display, line_color, [int(platform[0][0]), int(platform[0][1] - scroll)], 6, 2)
            pygame.draw.circle(display, line_color, [int(platform[1][0]), int(platform[1][1] - scroll)], 6, 2)

            if random.randint(0, 10) == 0:
                color = random.randint(150, 220)
                sparks.append([random.choice(platform), random.randint(0, 359), random.randint(7, 10) / 10, 5 * random.randint(5, 10) / 10, (color, color, color)])

    # 粒子(player) ------------------------------------------------- #
    particles.append(e.particle(player_pos, 'p', [random.randint(0, 20) / 40 - 0.25, random.randint(0, 10) / 15 - 1], 0.2, random.randint(0, 30) / 10, player_color))
    line_locations = check_line_sides(platforms, player_pos)

    start_pos = player_pos.copy()

    player_velocity[1] = min(player_terminal_velocity, player_velocity[1] + player_gravity)

    # 根據移動方向，更新粒子的位置
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]
    player_velocity[1] = normalize(player_velocity[1], 0.02)

    player_path.append(player_pos.copy())

    #　反彈冷卻
    if bounce_cooldown > 0:
        bounce_cooldown -= 1

    line_locations_post = check_line_sides(platforms, player_pos)

    for i, side in enumerate(line_locations):

        if sign(side) != sign(line_locations_post[i]): # 不同為正數 或是 不同為負數
            if sign(side) == -1: # 若是運動的方向是往下的

                if line_math.doIntersect([start_pos, player_pos], platforms[i]): # 判斷 粒子運動的路線是否跟白色線條有相交

                    if (player_pos[0] < display.get_width()) and (player_pos[0] > 0): # 如果粒子還在螢幕案為內

                        if bounce_cooldown == 0: # 反彈冷卻完畢

                            bounce_s.play() # 撥放撞擊的聲音

                            # 計算反彈的方向
                            angle = math.atan2(platforms[i][1][1] - platforms[i][0][1], platforms[i][1][0] - platforms[i][0][0])
                            normal = angle - math.pi * 0.5
                            bounce_angle = math.radians(mirror_angle(math.degrees(math.atan2(-player_velocity[1], -player_velocity[0])), math.degrees(normal)) % 360)

                            # 根據反彈的方向，變更粒子的運動方向
                            player_velocity[0] = math.cos(bounce_angle) * (dis_func(player_velocity) + 1)
                            player_velocity[1] = math.sin(bounce_angle) * (dis_func(player_velocity) + 1)
                            player_velocity[1] -= 2 * bounce_strength

                            # 生成 撞擊所產生的火花
                            for i in range(random.randint(4, 6)):
                                spark_angle = math.degrees(normal) + random.randint(0, 180) - 90
                                sparks.append([player_pos.copy(), spark_angle, (dis_func(player_velocity) + 1) / 3 * random.randint(7, 10) / 10, (dis_func(player_velocity) + 1) * 2 * random.randint(5, 10) / 10])

                            # 更新反彈冷卻  
                            bounce_cooldown = 3

    if (player_pos[0] < 0) or (player_pos[0] > display.get_width()): # 若粒子超出遊戲視窗範圍
        if end_game == False:
            death_s.play() # 播放死亡音效

            # 建立死亡時的畫面
            circle_effects.append([player_pos, 6, [6, 0.15], [10, 0.2], (190, 40, 100)]) 
            circle_effects.append([player_pos, 6, [6, 0.05], [5, 0.04], (190, 40, 100)])
            screen_shake = 12
        end_game = True

    # 遊戲背景的粒子 ---------------------------------------------- #
    for i, particle in sorted(enumerate(particles), reverse=True):
        alive = particle.update(1) # 檢查粒子是否還存活
        if not alive:
            particles.pop(i) # 超過壽命，pop出去
        else: 
            particle.draw(display, [0, scroll]) # 繪出粒子

    # GUI介面 ---------------------------------------------------- #
    font.render('score: ' + str(int(game_score)), gui_display, (game_text_loc, 4))
    font2.render(str(int(game_score)), gui_display, (display.get_width() // 2 - font.width(str(int(game_score))) // 2, end_text_loc + 4))
    font2.render('press R', gui_display, (display.get_width() // 2 - font.width('press R') // 2, end_text_loc + 28))
    font.render(str(int(game_score)), gui_display, (display.get_width() // 2 - font.width(str(int(game_score))) // 2, end_text_loc))
    font.render('press R', gui_display, (display.get_width() // 2 - font.width('press R') // 2, end_text_loc + 24))

    # 依據遊戲的狀況，更新文字顯示的位置
    if end_game:
        game_text_loc += (-120 - game_text_loc) / 20
        end_text_loc += (200 - end_text_loc) / 20
    else:
        game_text_loc += (6 - game_text_loc) / 10
        end_text_loc += (-220 - end_text_loc) / 20

    # 鍵盤、滑鼠按鈕事件 ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT: # 結束遊戲
            pygame.quit() 
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: # 結束遊戲
                pygame.quit()
                sys.exit()
            if event.key == K_r: # 遊戲結束，按下R從新開始
                if end_game:
                    restart_s.play()
                    transition = 30
                    lasers = []
                    line_effects = []
                    sparks = []
                    player_path = []
                    game_score = 0
                    end_game = False
                    particles = []
                    platforms = [[[0, display.get_height() - 1], [display.get_width(), display.get_height() - 1]]]
                    last_point = [display.get_width() // 2, display.get_height()]
                    scroll = 0
                    player_pos = [display.get_width() // 2, display.get_height() // 2]
                    player_velocity = [0, 0]
                    circle_effects = []
                    last_place = 50
                    square_effects = []

        if event.type == MOUSEBUTTONDOWN: # 如果事件是滑鼠被按下
            if event.button == 1: # 如果是滑鼠左鍵被按下
                if not end_game: # 如果遊戲還沒結束(end_game為遊戲結束)
                    # last point為紀錄滑鼠上次點擊的點
                    # [mx, my]為新的滑鼠點擊座標
                    # scroll為遊戲畫面上移的量
                    # platforms為紀錄所有線位置的list
                    line = [last_point, [mx, my + scroll]] # 線=上次點擊位置+新點擊位置
                    line.sort() # 依照x座標排序line的起始點跟終點
                    platforms.append(line) # 將新畫的line附加在platforms上
                    last_point = [mx, my + scroll] # 更新最後一次按下的座標位置

                    # circle紀錄特效的參數[[座標x,座標y], 半徑, [外框粗細,0.2], [縮放速度,0.3], [Red,Green,Blue]]
                    # circle_effects記錄所有的特效circle
                    circle = [[mx, my + scroll], 10, [4, 0.2], [4, 0.3], (0, 255, 255)] # 設定特效
                    circle_effects.append(circle) # 在按下的位置新增一個外擴圓的特效
                    place_s.play() # 播放place_s音效

    # Update ------------------------------------------------- #
    display_background = display.copy()
    display_background.set_alpha(25) # 背景透明度

    black_surf = pygame.Surface(screen.get_size())
    black_surf.fill(background_color)
    black_surf.set_alpha(85) # blur

    # 繪製陰影
    display.set_colorkey((background_color))
    screen.blit(pygame.transform.scale(display_background, (display.get_width() * 2 + 40, display.get_height() * 2 + 40)), (-20 + BORDER_WIDTH, 0))
    screen.blit(black_surf,(0, 0))

    offset = [0, 0]
    if screen_shake:
        offset[0] += random.randint(0, 10) - 5
        offset[1] += random.randint(0, 10) - 5

    # 將實體的線繪製在螢幕上
    # 若沒有此行，將繪只有陰影
    screen.blit(pygame.transform.scale(display, (display.get_width() * 2, display.get_height() * 2)), (BORDER_WIDTH + offset[0], offset[1]))

    #　將gui介面繪製在螢幕上
    screen.blit(pygame.transform.scale(gui_display, (display.get_width() * 2, display.get_height() * 2)),(BORDER_WIDTH, 0))
    
    # 繪製螢幕兩邊的黑色邊界
    border_box = pygame.Rect(0, 0, BORDER_WIDTH, screen.get_height())
    pygame.draw.rect(screen, (0, 0, 0), border_box)
    border_box.x = screen.get_width() - BORDER_WIDTH
    pygame.draw.rect(screen, (0, 0, 0), border_box)

    if transition:
        black_surf = pygame.Surface(screen.get_size())
        black_surf.set_alpha(255 * transition / 30)
        screen.blit(black_surf, (0, 0))

    pygame.display.update()
    mainClock.tick(60)
