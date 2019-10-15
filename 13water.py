# -*- coding: utf-8 -*-
import requests
import pygame
import json
import time
BLACKE = (0,0,0)
BLUE = (0,0,255)
pygame.init()
pygame.display.init()
def StartGame():
    window = background()
    window = window.newscreen()
    text_box_user = TextBox(270, 30, 525, 400, callback=callback)
    text_box_password = TextBox(270, 30, 525, 463, callback=callback)
    login_button = button(63,37,900,400)
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
                change(event.pos,text_box_user.getlist(),text_box_password.getlist())
                if login_button.mousepress(event.pos):
                    login(text_box_user.gettext(),text_box_password.gettext())
            elif event.type == pygame.KEYDOWN and  userinput:
                text_box_user.key_down(event)
            elif event.type == pygame.KEYDOWN and passwordinput:
                text_box_password.key_down(event)
        text_box_user.draw(window)
        text_box_password.draw(window)
        login_button.draw(window)  
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
        text_surf = self.font.render(self.text, True, (255,255,255))
        dest_surf.blit(self.__surface, (self.x, self.y))
        dest_surf.blit(text_surf,(self.x+5, self.y + (self.height - text_surf.get_height())),
                       (0, 0, self.width-5, self.height))
 
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
    def getlist(self):
        list = [self.x,self.y,self.width,self.height]
        return list 
    def gettext(self):
        return self.text
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

def change(rect,userlist,passwordlist):
    x,y = rect
    global userinput
    global passwordinput
    if x>userlist[0] and x<userlist[0]+userlist[2] and y>userlist[1] and y<userlist[1]+userlist[3]:
        userinput = True
    else:
        userinput = False   
    if x>passwordlist[0] and x<passwordlist[0]+passwordlist[2] and y>passwordlist[1] and y<passwordlist[1]+passwordlist[3]:
        passwordinput = True
    else:
        passwordinput =False

def login(user,password):
    url = "https://api.shisanshui.rtxux.xyz/auth/login"
    payload = "{\"username\":\""+user+"\",\"password\":\""+password+"\"}"
    headers = {'content-type': 'application/json'}
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

class button():
    def __init__(self,w,h,x,y,font='fdbsjw.ttf'):
        """ 
        w:按钮的宽度
        h:按钮的高度
        x:按钮的x坐标
        y:按钮的y坐标
        """
        self.width = w
        self.height = h
        self.x  = x
        self.y  = y
        self.font = pygame.font.Font(font,31)
        self.__surface = pygame.Surface((w,h))
        self.rect = self.__surface.get_rect()
        self.rect[0] = self.x
        self.rect[1] = self.y
    def draw(self,dest_surf):
        text_surf = self.font.render('登陆',True,(0,255,0))
        dest_surf.fill((50,50,255),self.rect)
        dest_surf.blit(text_surf,(self.x,self.y))
    def mousepress(self,rect):
        x,y = rect
        if x>self.x and x<self.x+self.width and y>self.y and y<self.y+self.height:
            return True
        else:
            return False
def register():
    pass





if __name__ == "__main__":
    StartGame()