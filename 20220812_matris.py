#!/usr/bin/env python
import pygame
from pygame import Rect, Surface
import random
import os
import kezmenu

from tetrominoes import list_of_tetrominoes
from tetrominoes import rotate

from scores import load_score, write_score # 從scores.py匯入load_score、write_score函式

import sys
# from sys import argv, exit 

class GameOver(Exception):
    """Exception used for its control flow properties"""

def get_sound(filename):
    return pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "resources", filename))

BGCOLOR = (15, 15, 20)	#背景顏色
BORDERCOLOR = (140, 140, 140)	#邊框顏色

BLOCKSIZE = 30 # 方框的大小
BORDERWIDTH = 10 # 邊框粗細

MATRIS_OFFSET = 20

MATRIX_WIDTH = 10 # 一列可放的方塊數量
MATRIX_HEIGHT = 22# 一行可放的方塊數量

LEFT_MARGIN = 340

WIDTH = MATRIX_WIDTH*BLOCKSIZE + BORDERWIDTH*2 + MATRIS_OFFSET*2 + LEFT_MARGIN #視窗的寬度
HEIGHT = (MATRIX_HEIGHT-2)*BLOCKSIZE + BORDERWIDTH*2 + MATRIS_OFFSET*2 #視窗的長度

TRICKY_CENTERX = WIDTH-(WIDTH-(MATRIS_OFFSET+BLOCKSIZE*MATRIX_WIDTH+BORDERWIDTH*2))/2

VISIBLE_MATRIX_HEIGHT = MATRIX_HEIGHT - 2 #可見方塊的寬度


class Matris(object):
    # __init__(slef, 第幾關, 分數, 消除幾行, 連擊, 暫停, 最高分, 音效)
    def __init__(self, level, score, lines, combo, paused, highscore, played_highscorebeaten_sound):
        self.surface = screen.subsurface(Rect((MATRIS_OFFSET+BORDERWIDTH, MATRIS_OFFSET+BORDERWIDTH),
                                              (MATRIX_WIDTH * BLOCKSIZE, (MATRIX_HEIGHT-2) * BLOCKSIZE)))

        self.matrix = dict()
        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):
                self.matrix[(y,x)] = None
        #-------------------------------------------------------------------------
        # matrix的狀態偵測
        #   self.matrix                 :紀錄面板上被多少方塊占用(不包括正在墜落的方塊)
        #   self.set_tetrominoes        :管理正在墜落的方塊
        #   self.level                  :遊戲難度(影響速度)
        #   self.base_downwards_speed   :下降速度，數字越高下降速度越慢 預設400ms
        #-------------------------------------------------------------------------


        self.next_tetromino = random.choice(list_of_tetrominoes) # 隨機決定下一個方塊
        self.set_tetrominoes() 
        self.tetromino_rotation = 1 
        self.downwards_timer = 0 #block下降的計時器
        self.base_downwards_speed = 0.4 # 

        self.movement_keys = {'left': 0, 'right': 0}    # 紀錄按鍵按下
        self.movement_keys_speed = 0.05
        self.movement_keys_timer = (-self.movement_keys_speed)*2

        self.level = level # 將分數封裝進class
        self.score = score # 將分數封裝進class
        self.lines = lines # 將消除幾行封裝進class
        self.combo = combo # 將連擊數封裝進class
        self.paused = paused # 將是否暫停的狀態封裝進class
        self.highscore = highscore  # 將最最高分紀錄封裝進class
        # 將是否要播放音效的狀態封裝進class
        self.played_highscorebeaten_sound = played_highscorebeaten_sound

        # 設定各式音效
        self.levelup_sound  = get_sound("levelup.wav")
        self.gameover_sound = get_sound("gameover.wav")
        self.linescleared_sound = get_sound("linecleared.wav")
        self.highscorebeaten_sound = get_sound("highscorebeaten.wav")


    def set_tetrominoes(self): #OK
        #-------------------------------------------------------------------------
        # 設定當前的方塊和下一個方塊
        #   self.current_tetromino                      :當前方塊
        #   self.next_tetromino                         :下一個方塊
        #   self.surface_of_next_tetromino              :下一個方塊的圖形
        #   self.construct_surface_of_next_tetromino    :建構下一個方塊圖形
        #   self.tetromino_position                     :方塊位置
        #   self.tetromino_rotation                     :旋轉角度
        #   self.tetromino_block                        :方塊的樣子和顏色
        #-------------------------------------------------------------------------
        self.current_tetromino = self.next_tetromino #現在的方塊，等於上次的下一個方塊
        self.next_tetromino = random.choice(list_of_tetrominoes) #隨機決定下一個方塊
        self.surface_of_next_tetromino = self.construct_surface_of_next_tetromino()
        self.tetromino_position = (0,4) if len(self.current_tetromino.shape) == 2 else (0, 3)
        self.tetromino_rotation = 0
        self.tetromino_block = self.block(self.current_tetromino.color)
        self.shadow_block = self.block(self.current_tetromino.color, shadow=True)

    
    def hard_drop(self): #OK
        #-------------------------------------------------------------------------
        #   立刻放下方塊
        #-------------------------------------------------------------------------
        amount = 0
        while self.request_movement('down'):
            amount += 1
        self.score += 10*amount

        self.lock_tetromino() #方塊下降後，檢查是否可消除方塊


    def update(self, timepassed): #OK
        #-------------------------------------------------------------------------
        #   主要程式迴圈
        #-------------------------------------------------------------------------
        self.needs_redraw = False 
        
        pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key #lambda函式，定義按下鍵盤
        unpressed = lambda key: event.type == pygame.KEYUP and event.key == key #lambda函式，定義鬆開按鍵

        events = pygame.event.get()
        #偵測暫停和離開遊戲
        for event in events:
            if pressed(pygame.K_p): #按下P暫停遊戲
                self.surface.fill((0,0,0)) #遊戲背景設為黑色
                self.needs_redraw = True #設定為需要重新渲染畫布
                self.paused = not self.paused 
            elif event.type == pygame.QUIT:
                self.gameover(full_exit=True)
            elif pressed(pygame.K_ESCAPE): #按下exsapce回到主選單
                self.gameover()

        if self.paused:
            return self.needs_redraw

        for event in events:
          
            if pressed(pygame.K_UP): # 如果按向上鍵
                self.request_rotation() # 旋轉方塊
            elif pressed(pygame.K_LEFT): # 如果按向左鍵
                self.request_movement('left') # 移動方塊(往左)
                self.movement_keys['left'] = 1
            elif pressed(pygame.K_RIGHT): #如果按向右鍵
                self.request_movement('right') # 移動方塊(往右)
                self.movement_keys['right'] = 1

            elif unpressed(pygame.K_LEFT) or unpressed(pygame.K_a):
                self.movement_keys['left'] = 0
                self.movement_keys_timer = (-self.movement_keys_speed)*2
            elif unpressed(pygame.K_RIGHT) or unpressed(pygame.K_d):
                self.movement_keys['right'] = 0
                self.movement_keys_timer = (-self.movement_keys_speed)*2
            
            if pressed(pygame.K_SPACE): # 如果按下空白鍵
                self.hard_drop() # 方塊直接下降到底部



        self.downwards_speed = self.base_downwards_speed ** (1 + self.level/10.)    #方塊下降的速度，根據關卡上升而加快

        self.downwards_timer += timepassed #下降計時器 + 每一幀的時間

        # 如果按下方向鍵向下或是S，下降的速度乘0.1
        downwards_speed = self.downwards_speed*0.10 if any([pygame.key.get_pressed()[pygame.K_DOWN],
                                                            pygame.key.get_pressed()[pygame.K_s]]) else self.downwards_speed

        if self.downwards_timer > downwards_speed:
            if not self.request_movement('down'): #放下方塊或疊在其他方塊上
                self.lock_tetromino() #檢查是否可以消除方塊

            self.downwards_timer %= downwards_speed


        if any(self.movement_keys.values()):
            self.movement_keys_timer += timepassed

        if self.movement_keys_timer > self.movement_keys_speed:
            self.request_movement('right' if self.movement_keys['right'] else 'left')
            self.movement_keys_timer %= self.movement_keys_speed
        
        return self.needs_redraw

    def draw_surface(self): #OK
        #-------------------------------------------------------------------------
        #   繪製出遊戲圖示
        # 	根據每格的狀態畫出背景或是shadow、block
        #-------------------------------------------------------------------------
        with_tetromino = self.blend(matrix=self.place_shadow()) #獲得每隔的狀態

        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):

                #作者隱藏了兩排在畫面外，方塊會在畫面外先形成
                block_location = Rect(x*BLOCKSIZE, (y*BLOCKSIZE - 2*BLOCKSIZE), BLOCKSIZE, BLOCKSIZE)

                if with_tetromino[(y,x)] is None: #該格不是被標註為方塊或是shadow，則填入背景顏色
                    self.surface.fill(BGCOLOR, block_location)
                else:
                    if with_tetromino[(y,x)][0] == 'shadow': # 若為shadow 則先填入背景顏色
                        self.surface.fill(BGCOLOR, block_location)
                    
                    self.surface.blit(with_tetromino[(y,x)][1], block_location) #畫出方塊以及shadow
                    
    def gameover(self, full_exit=False): #OK
        #-------------------------------------------------------------------------
        #   遊戲結束偵測
        #       當新的方塊產生但不符合版面上的結果產生遊戲結束。
        #       self.lock_tetromino負責檢測方塊掉落後是否結束
        #-------------------------------------------------------------------------

        write_score(self.score) # 將成績寫到檔案中
        
        if full_exit:  # 遊戲結束，並關閉式窗
            pygame.quit()
            sys.exit()
        else:
            raise GameOver("Sucker!")

    def place_shadow(self): #OK
        #-------------------------------------------------------------------------
        #   畫出shadow
        #-------------------------------------------------------------------------
        posY, posX = self.tetromino_position #獲得方塊的位置

        while self.blend(position=(posY, posX)): #計算shadow的位置
            posY += 1

        position = (posY-1, posX)

        return self.blend(position=position, shadow=True) #檢查shodow的位置是否合法

    def fits_in_matrix(self, shape, position): #OK
        #-------------------------------------------------------------------------
        #	檢查旋轉後的方塊是否超出範圍，
        #	超出範圍 	回傳false
        #	沒有超出範圍 回傳旋轉後的位置
        #-------------------------------------------------------------------------
        posY, posX = position
        for x in range(posX, posX+len(shape)):
            for y in range(posY, posY+len(shape)):
                if self.matrix.get((y, x), False) is False and shape[y-posY][x-posX]: # 若超出邊界，回傳false
                    return False

        return position
                    
    def request_rotation(self): #OK
        #-------------------------------------------------------------------------
        #   檢查方塊是否能夠旋轉，如果可以則回傳旋轉後的位置
        #-------------------------------------------------------------------------
        rotation = (self.tetromino_rotation +1) 
        shape = self.rotated(rotation)

        y, x = self.tetromino_position

        # 獲得旋轉後的位置
        position = (self.fits_in_matrix(shape, (y, x)) or
                    self.fits_in_matrix(shape, (y, x+1)) or
                    self.fits_in_matrix(shape, (y, x-1)) or
                    self.fits_in_matrix(shape, (y, x+2)) or
                    self.fits_in_matrix(shape, (y, x-2)))

        if position and self.blend(shape, position): # 如果可以旋轉，且旋轉後的位置是合法的，則更新位置
            self.tetromino_rotation = rotation
            self.tetromino_position = position
            
            self.needs_redraw = True
            return self.tetromino_rotation
        else:
            return False
            
    def request_movement(self, direction): #OK
       	#-------------------------------------------------------------------------
        #   檢查是否還有空間提供方塊移動(左右、下降、旋轉)，如果可以，則回傳新位置
        #-------------------------------------------------------------------------
        posY, posX = self.tetromino_position #獲得現在的位置

        if direction == 'left' and self.blend(position=(posY, posX-1)): #向左移動
            self.tetromino_position = (posY, posX-1)
            self.needs_redraw = True
            return self.tetromino_position
        elif direction == 'right' and self.blend(position=(posY, posX+1)): #向右移動
            self.tetromino_position = (posY, posX+1)
            self.needs_redraw = True
            return self.tetromino_position
        elif direction == 'up' and self.blend(position=(posY-1, posX)): #旋轉
            self.needs_redraw = True
            self.tetromino_position = (posY-1, posX)
            return self.tetromino_position
        elif direction == 'down' and self.blend(position=(posY+1, posX)): #下降
            self.needs_redraw = True
            self.tetromino_position = (posY+1, posX)
            return self.tetromino_position
        else:
            return False

    def rotated(self, rotation=None): #OK
        #-------------------------------------------------------------------------
        # 	旋轉方塊
        #-------------------------------------------------------------------------

        if rotation is None:
            rotation = self.tetromino_rotation
        return rotate(self.current_tetromino.shape, rotation)

    def block(self, color, shadow=False): #OK
        #-------------------------------------------------------------------------
        #	設定方塊的屬性
        #-------------------------------------------------------------------------

        colors = {'blue':   (105, 105, 255),
                  'yellow': (225, 242, 41),
                  'pink':   (242, 41, 195),
                  'green':  (22, 181, 64),
                  'red':    (204, 22, 22),
                  'orange': (245, 144, 12),
                  'cyan':   (10, 255, 226)}


        if shadow: # 如果是shadow 邊線與方塊都變淺 (rgb各加90)
            end = [90]  
        else:
            end = [] 

        border = Surface((BLOCKSIZE, BLOCKSIZE), pygame.SRCALPHA, 32) # 建立一個方塊大小的畫布

        border.fill(list(map(lambda c: c*0.5, colors[color])) + end)    # 設定邊界顏色
        borderwidth = 2 # 設定邊界粗細

        box = Surface((BLOCKSIZE-borderwidth*2, BLOCKSIZE-borderwidth*2), pygame.SRCALPHA, 32) # 建立一個扣除邊界的方塊畫布
        boxarr = pygame.PixelArray(box) #使用PixalArray將box以像素的方式呈現

        # 將每個pixal填上顏色
        for x in range(len(boxarr)):
            for y in range(len(boxarr)):
                boxarr[x][y] = tuple(list(map(lambda c: min(255, int(c*random.uniform(0.8, 1.2))), colors[color])) + end) 

        del boxarr  #刪除PixelArray，釋放boxarr

        border.blit(box, Rect(borderwidth, borderwidth, 0, 0)) # 將兩塊畫布重疊


        return border # 回傳畫布

    def lock_tetromino(self): #OK
        #-------------------------------------------------------------------------
        #   當方塊落下後要消除，更新self.matrix計算分數、行數等，創建新的方塊
        #-------------------------------------------------------------------------
        self.matrix = self.blend()

        lines_cleared = self.remove_lines() #消除完成一排的方塊，且回傳消除的行數
        self.lines += lines_cleared #更新消除的總行數

        if lines_cleared:
            if lines_cleared >= 4: #一次消超過4行，放出音效
                self.linescleared_sound.play()
            self.score += 100 * (lines_cleared**2) * self.combo #根據消除的行數、combo數 更新分數

            if not self.played_highscorebeaten_sound and self.score > self.highscore: # 沒有其他音效 且 超越最高分，則放出音效
                if self.highscore != 0:
                    self.highscorebeaten_sound.play()
                self.played_highscorebeaten_sound = True

        if self.lines >= self.level*10: # 更新等級 且 放出音效
            self.levelup_sound.play()
            self.level += 1

        self.combo = self.combo + 1 if lines_cleared else 1 # 更新combo數

        self.set_tetrominoes() #開始下一個方塊

        if not self.blend(): #無法再放入更多方塊，則結束遊戲
            self.gameover_sound.play()
            self.gameover()
            
        self.needs_redraw = True

    def remove_lines(self): #OK
        #-------------------------------------------------------------------------
        #   將完成的線從版面上移除
        #-------------------------------------------------------------------------
        lines = []
        for y in range(MATRIX_HEIGHT):
            #檢查每一行是否完成
            line = (y, [])
            for x in range(MATRIX_WIDTH):
                if self.matrix[(y,x)]:
                    line[1].append(x)
            if len(line[1]) == MATRIX_WIDTH:
                lines.append(y)

        for line in sorted(lines):
            #將行往下移一層
            for x in range(MATRIX_WIDTH):
                self.matrix[(line,x)] = None
            for y in range(0, line+1)[::-1]:
                for x in range(MATRIX_WIDTH):
                    self.matrix[(y,x)] = self.matrix.get((y-1,x), None)

        return len(lines)

    def blend(self, shape=None, position=None, matrix=None, shadow=False): #OK
        #-------------------------------------------------------------------------
        #   1. 檢查在線上的形狀是否完整，如果是的話則copy matrix，否則false
        #   2. 檢測玩家操作是否合法(有無超出左右界線、是否以堆疊到頂部)
        # 	3. 也用來在self.draw_surface繪製落下方塊與shadow
        #  	4. copy用來記錄(x,y)的狀態，shadow、block或是NULL
        #-------------------------------------------------------------------------
        if shape is None:
            shape = self.rotated()
        if position is None:
            position = self.tetromino_position

        copy = dict(self.matrix if matrix is None else matrix)
        posY, posX = position
        for x in range(posX, posX+len(shape)):
            for y in range(posY, posY+len(shape)):
                if (copy.get((y, x), False) is False and shape[y-posY][x-posX] # 若 方塊超出左右範圍 或是 已經堆疊到頂部 則回傳false
                    or copy.get((y,x)) and shape[y-posY][x-posX] and copy[(y,x)][0] != 'shadow'): 

                    return False # 該次的操作是不合法的，回傳false

                elif shape[y-posY][x-posX]: 
                    copy[(y,x)] = ('shadow', self.shadow_block) if shadow else ('block', self.tetromino_block)

        return copy 

    def construct_surface_of_next_tetromino(self): #OK
        #-------------------------------------------------------------------------
        #   繪製下個方塊的圖形
        #-------------------------------------------------------------------------
        shape = self.next_tetromino.shape  #獲得方塊得形狀
        surf = Surface((len(shape)*BLOCKSIZE, len(shape)*BLOCKSIZE), pygame.SRCALPHA, 32) #建議一個方塊大小的畫布

        for y in range(len(shape)):
            for x in range(len(shape)):
                if shape[y][x]:
                    surf.blit(self.block(self.next_tetromino.color), (x*BLOCKSIZE, y*BLOCKSIZE)) #在畫布上繪製顏色
        
        return surf #回傳畫好的物件

class Game(object):
    def main(self, screen): #OK
        #-------------------------------------------------------------------------
        #   遊戲主循環
        #-------------------------------------------------------------------------

        clock = pygame.time.Clock()
        
        # 建立一個Matris的物件(第幾關, 分數, 消除幾行, 連擊, 暫停, 最高分, 最高分音效)
        self.matris = Matris(1, 0, 0, 0, False, load_score(), False) 
        
        screen.blit(construct_nightmare(screen.get_size()), (0,0))
        

        matris_border = Surface((MATRIX_WIDTH*BLOCKSIZE+BORDERWIDTH*2, VISIBLE_MATRIX_HEIGHT*BLOCKSIZE+BORDERWIDTH*2))
        matris_border.fill(BORDERCOLOR) # 設定遊戲框的邊界
        screen.blit(matris_border, (MATRIS_OFFSET,MATRIS_OFFSET)) # 畫出遊戲框的邊界
        
        self.redraw() # 繪畫遊戲畫面

        while True:
            try:
                timepassed = clock.tick(50)
                if self.matris.update((timepassed / 1000.) if not self.matris.paused else 0):
                    self.redraw()
            except GameOver:
                return
      
    def redraw(self): #OK
        #-------------------------------------------------------------------------
        #   調用繪製面板的函式
        #-------------------------------------------------------------------------
        if not self.matris.paused:
            self.blit_next_tetromino(self.matris.surface_of_next_tetromino) # 畫出下一個方塊
            self.blit_info() # 畫出遊戲資訊 分數、combo數等等

            self.matris.draw_surface() # 畫出主遊戲區域

        pygame.display.flip() #更新畫面


    def blit_info(self): #OK
        #-------------------------------------------------------------------------
        #   繪製資訊面板
        #-------------------------------------------------------------------------
        textcolor = (255, 255, 255) # 字體顏色
        font = pygame.font.Font(None, 30) #設定字體
        width = (WIDTH-(MATRIS_OFFSET+BLOCKSIZE*MATRIX_WIDTH+BORDERWIDTH*2)) - MATRIS_OFFSET*2 #隨著視窗大小變動字體大小

        def renderpair(text, val):
            text = font.render(text, True, textcolor)
            val = font.render(str(val), True, textcolor)

            surf = Surface((width, text.get_rect().height + BORDERWIDTH*2), pygame.SRCALPHA, 32)

            surf.blit(text, text.get_rect(top=BORDERWIDTH+10, left=BORDERWIDTH+10))
            surf.blit(val, val.get_rect(top=BORDERWIDTH+10, right=width-(BORDERWIDTH+10)))
            return surf
        
        #調整側邊資訊欄大小以允許所有資訊能夠正常顯示
        scoresurf = renderpair("Score", self.matris.score)
        levelsurf = renderpair("Level", self.matris.level)
        linessurf = renderpair("Lines", self.matris.lines)
        combosurf = renderpair("Combo", "x{}".format(self.matris.combo))

        height = 20 + (levelsurf.get_rect().height + 
                       scoresurf.get_rect().height +
                       linessurf.get_rect().height + 
                       combosurf.get_rect().height )
        
        #側邊資訊欄的顏色
        area = Surface((width, height))
        area.fill(BORDERCOLOR)
        area.fill(BGCOLOR, Rect(BORDERWIDTH, BORDERWIDTH, width-BORDERWIDTH*2, height-BORDERWIDTH*2))
        
        #繪製側邊資訊欄
        area.blit(levelsurf, (0,0))
        area.blit(scoresurf, (0, levelsurf.get_rect().height))
        area.blit(linessurf, (0, levelsurf.get_rect().height + scoresurf.get_rect().height))
        area.blit(combosurf, (0, levelsurf.get_rect().height + scoresurf.get_rect().height + linessurf.get_rect().height))

        screen.blit(area, area.get_rect(bottom=HEIGHT-MATRIS_OFFSET, centerx=TRICKY_CENTERX))


    def blit_next_tetromino(self, tetromino_surf): #OK
        #-------------------------------------------------------------------------
        #   把下一個方塊繪製在側邊介面中
        #-------------------------------------------------------------------------
        area = Surface((BLOCKSIZE*5, BLOCKSIZE*5)) #宣告一個5*5的畫布
        area.fill(BORDERCOLOR) 
        area.fill(BGCOLOR, Rect(BORDERWIDTH, BORDERWIDTH, BLOCKSIZE*5-BORDERWIDTH*2, BLOCKSIZE*5-BORDERWIDTH*2))

        areasize = area.get_size()[0] # 取得畫布的大小
        tetromino_surf_size = tetromino_surf.get_size()[0] # 取的方塊的大小
        

        center = areasize/2 - tetromino_surf_size/2 # 計算放方塊的中心點
        area.blit(tetromino_surf, (center, center)) # 在area上繪製方塊

        screen.blit(area, area.get_rect(top=MATRIS_OFFSET, centerx=TRICKY_CENTERX)) # 將area繪製於screen上

class Menu(object): #OK
    #-------------------------------------------------------------------------
    #   創建主選單
    #-------------------------------------------------------------------------

    running = True
    def main(self, screen):
        clock = pygame.time.Clock()
        menu = kezmenu.KezMenu( # 創建選項
            ['Play!', lambda: Game().main(screen)], #呼叫Game中的main函式 開始遊戲
            #['Quit', lambda: setattr(self, 'running', False)], #離開遊戲
        )
        menu.position = (50, 50)  # 設置文字顯示的位置
        menu.enableEffect('enlarge-font-on-focus', font=None, size=60, enlarge_factor=1.2, enlarge_time=0.3) #放大focus的選項
        menu.color = (255,255,255) # 設定選項字體為白色
        menu.focus_color = (40, 200, 40) # 被focus的字體為綠色
        
        nightmare = construct_nightmare(screen.get_size()) # 隨機生成背景的方塊顏色
        highscoresurf = self.construct_highscoresurf() #讀取最高的成績

        timepassed = clock.tick(30) / 1000. #計算每一幀的時間

        while self.running:
            events = pygame.event.get() # 獲得play 或是 Quit 事件

            for event in events: 
                if event.type == pygame.QUIT: # 事件為Quit則結束遊戲
                    pygame.quit()
                    sys.exit()

            # 事件為play
            menu.update(events, timepassed) #開始遊戲

            timepassed = clock.tick(30) / 1000.

            if timepassed > 1: 
                highscoresurf = self.construct_highscoresurf()

            screen.blit(nightmare, (0,0)) #畫出背景
            screen.blit(highscoresurf, highscoresurf.get_rect(right=WIDTH-50, bottom=HEIGHT-50)) # 畫出最高成績
            menu.draw(screen)  # 顯現在視窗上
            pygame.display.flip() # 更新畫布

    def construct_highscoresurf(self): #OK
        #-------------------------------------------------------------------------
        #   從檔案讀取最高的成績
        #-------------------------------------------------------------------------
        font = pygame.font.Font(None, 50) #設定文字樣式
        highscore = load_score() #獲得最高分數
        text = "Highscore: {}".format(highscore) # 將最高分與"Highscore："串接
        return font.render(text, True, (255,255,255)) #回傳最高成績

def construct_nightmare(size): #OK
    #-------------------------------------------------------------------------
    #   建立背景圖片
    #-------------------------------------------------------------------------

    surf = Surface(size) #建立一個surface

    boxsize = 8 #設定方塊大小
    bordersize = 1 #設定方塊邊界粗細
    vals = '1235' # 更改背景的彩度
    arr = pygame.PixelArray(surf) #使用PixalArray將surf以像素的方式呈現
    for x in range(0, len(arr), boxsize): 
        for y in range(0, len(arr[x]), boxsize):
        	# 隨機生成顏色
            color = int(''.join([random.choice(vals) + random.choice(vals) for _ in range(3)]), 16) 

            # 將每個pixal填上顏色
            for LX in range(x, x+(boxsize - bordersize)):
                for LY in range(y, y+(boxsize - bordersize)):
                    if LX < len(arr) and LY < len(arr[x]):
                        arr[LX][LY] = color
    del arr #刪除PixelArray，釋放Surf
    return surf #回傳完成繪畫的背景


if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.init() #pygmae 初始

    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 根據長寬初始化視窗

    pygame.display.set_caption("MATRIS") # 設定視窗的名稱

    Menu().main(screen) # 呼叫Menu中的main 函式
