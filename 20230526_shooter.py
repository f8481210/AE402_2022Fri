import pygame
from pygame.constants import TIMER_RESOLUTION
class Shooter:
    position = pygame.Vector2() # 彈弓位置(x, y)
    width = 70 # 彈弓寬度
    height = 67 # 彈弓高度
    direction = 0 # 方向初始化
    hasBullet = True # 是否還有剩餘的子彈
    def __init__(self):
        self.position.xy = 320 - self.width/2, 400 # 初始化彈弓位置
    def setDirection(self, direction):
        self.direction = direction # 設定彈弓移動方向
    def update(self, dt):
        # self.direction 紀錄彈弓移動方向(-1往左, 0不動, 1往右)
        self.direction = 0 # 方向初始化
        keys = pygame.key.get_pressed() # 取得按鍵
        if keys[pygame.K_LEFT]: # 如果是左鍵
            self.direction = -1 # 方向設定為左
        if keys[pygame.K_RIGHT]: # 如果是右鍵
            self.direction = 1 # 方向設定為右
        
        # self.position.x 為彈弓x軸位置數值
        # self.position.y 為彈弓y軸位置數值
        # self.position.xy 為彈弓在座標軸中的位置(x, y)
        if (self.position.x > 0 and self.direction == -1) or \
            (self.position.x < 640-self.width and self.direction == 1): # 前進的方向沒有超出邊界
            self.position.xy = (self.position.x + self.direction*3 , self.position.y) # 設定移動後的位置
    def reset(self):
        self.direction = 0 # 重新設定彈弓移動方向
        self.hasBullet = True # 重新設定是否還有剩餘的子彈
        self.position.xy = 320 - self.width/2 , 400 # 重新設定彈弓位置(x, y)
        
        