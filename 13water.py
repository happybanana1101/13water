# -*- coding: utf-8 -*-
import requests
import pygame
import json
import time
import http.client
global userinput
global passwordinput
userinput = False
passwordinput = False
BLACKE = (0,0,0)
pygame.init()
pygame.display.init()
def StartGame():
    window = background()
    window = window.newscreen()
    text_box_user = TextBox(270, 30, 525, 400, callback=callback)
    text_box_password = TextBox(270, 30, 525, 463, callback=callback)
    while True:
        time.sleep(0.01)
        # window = background()
        # window = window.newscreen()
        # text_box_user = TextBox(270, 30, 525, 400, callback=callback)
        # text_box_password = TextBox(270, 30, 525, 463, callback=callback)
        eventlist = pygame.event.get()

        for event in eventlist:
            if event.type == pygame.QUIT:
                Endgame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                change(event.pos,text_box_user.rect(),text_box_password.rect(),userinput,passwordinput)
            elif event.type == pygame.KEYDOWN and  userinput:
                print(1)
                text_box_user.key_down(event)
            elif event.type == pygame.KEYDOWN and passwordinput:
                # print(2)
                text_box_password.key_down(event)

        text_box_user.draw(window)
        text_box_password.draw(window)     
        pygame.display.update()

def Endgame():
    exit()


class TextBox:
    def __init__(self, w, h, x, y, font=None ,callback=None):
        """
        :param w:文本框宽度
        :param h:文本框高度
        :param x:文本框坐标
        :param y:文本框坐标
        :param font:文本框中使用的字体
        :param callback:在文本框按下回车键之后的回调函数
        """
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.text = ""  # 文本框内容
        self.callback = callback
        self.rect = None #文本框矩形区域
        # 创建
        self.__surface = pygame.Surface((w, h))
        self.rect = self.__surface.get_rect()
        self.font = pygame.font.Font(None, 31)  
 
    def draw(self,dest_surf):
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        dest_surf.blit(self.__surface, (self.x, self.y))
        dest_surf.blit(text_surf,(self.x, self.y + (self.height - text_surf.get_height())),
                       (0, 0, self.width, self.height))
 
    def key_down(self,event):
        unicode = event.unicode
        key = event.key
 
        # 退位键
        if key == 8:
            self.text = self.text[:-1]
            return
 
        # 切换大小写键
        if key == 301:
            return
 
        # 回车键
        if key == 13:
            if self.callback is not None:
                self.callback()
            return
 
        if unicode != "":
            char = unicode
        else:
            char = chr(key)
        self.text += char
    def getrect(self):
        return self.rect
 
def callback():
    print("回车测试")
 

class background():
    def __init__(self): 
        pass
    def newscreen(self):
        screen = pygame.display.set_mode([1280,591])   #设置窗口大小
        pygame.display.set_caption('13water')  #设置窗口标题
        back = pygame.image.load("background.jpg")
        screen.blit(back,(0,0))
        text1,text2 = background.Textsurface()
        screen.blit(text1,(420,400))
        screen.blit(text2,(420,460))
        return screen
    def Textsurface():
        pygame.font.init()
        font = pygame.font.Font("fdbsjw.ttf",30)
        textsurface1 = font.render('用户名:',True,BLACKE)
        textsurface2 = font.render('密   码:',True,BLACKE)
        return textsurface1,textsurface2

def change(rect,user,password,userinput,passwordinput):
    print(user)
    print(password)
    








if __name__ == "__main__":
    StartGame()