# -*- coding: utf-8 -*-
import requests
import pygame
import json
import time
import ai
BLACKE = (0, 0, 0)
BLUE = (0, 0, 255)
pygame.init()
pygame.display.init()
userinput = False
passwordinput = False
def StartGame():
    home_surface = False
    game_surface = False
    login_surface = True
    ranking_surface = False
    history_surface = False
    while True:
        if login_surface: #登陆界面
            window = background()
            window = window.newscreen()
            text_box_user = TextBox(270, 30, 525, 400, callback=callback)
            text_box_password = TextBox(270, 30, 525, 463, callback=callback)
            login_botton = button(63, 37, 900, 400, '登陆')
            register_button = button(63, 37, 900, 460, '注册')
            while login_surface:
                eventlist = pygame.event.get()
                for event in eventlist:
                    if event.type == pygame.QUIT:
                        Endgame()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        change(event.pos, text_box_user.getlist(),
                        text_box_password.getlist())
                        if login_botton.mousepress(event.pos):
                            login_class = Login(text_box_user.gettext(), text_box_password.gettext())
                            login_class.login()
                            if login_class.response_statue_code == 200:
                                home_surface = True
                                login_surface = False
                                break
                        elif register_button.mousepress(event.pos):
                            register(text_box_user.gettext(),text_box_password.gettext())
                    elif event.type == pygame.KEYDOWN and userinput:
                        text_box_user.key_down(event)
                    elif event.type == pygame.KEYDOWN and passwordinput:
                        text_box_password.key_down(event)
                text_box_user.draw(window)
                text_box_password.draw(window)
                login_botton.draw(window)
                register_button.draw(window)
                pygame.display.update()
        elif home_surface:  #主界面
            backsurface = pygame.image.load("background.jpg")
            window.blit(backsurface,(0,0))
            start_button = button(126,37,370,400,"开始游戏")
            history_button = button(126,37,570,400,"历史战绩")
            rankingbutton = button(94,37,770,400,"排行榜")
            start_button.draw(window)
            history_button.draw(window)
            rankingbutton.draw(window)
            pygame.display.update()
            while home_surface:
                time.sleep(0.01)
                eventlist = pygame.event.get()
                for event in eventlist:
                    if event.type == pygame.QUIT:
                        Endgame()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if start_button.mousepress(event.pos):
                            home_surface = False
                            game_surface = True
                            break
                        elif history_button.mousepress(event.pos):
                            home_surface = False
                            history_surface = True
                            break
                        elif rankingbutton.mousepress(event.pos):
                            home_surface = False
                            ranking_surface = True
                            break
        elif game_surface: #出牌界面
            backsurface = pygame.image.load("未标题-1.jpg")
            window.blit(backsurface,(0,0))
            playcard_button = button(63,37,570,400,"出牌")
            return_button = button(63,37,0,0,"返回")
            playcard_button.draw(window)
            return_button.draw(window)
            pygame.display.update()
            while game_surface:
                time.sleep(0.01)
                eventlist = pygame.event.get()
                for event in eventlist:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if playcard_button.mousepress(event.pos):
                            for i in range(0,50):
                                chupai(login_class)
                        elif return_button.mousepress(event.pos):
                            home_surface = True
                            game_surface = False
                            break
                    elif event.type == pygame.QUIT:
                        Endgame()

        elif ranking_surface: #排行榜界面
            backsurface = pygame.image.load("background.jpg")
            window.blit(backsurface,(0,0))
            titlefont = pygame.font.Font('fdbsjw.ttf',40)
            title_surface = titlefont.render("名次           ID                分数",True,BLACKE)
            rankfont = pygame.font.Font("fdbsjw.ttf",20)
            lastpage_button = button(94,37,900,400,"上一页")
            nextpage_button = button(94,37,900,460,'下一页')
            lastpage_button.draw(window)
            nextpage_button.draw(window)
            return_button = button(63,37,0,0,"返回")
            return_button.draw(window)
            pygame.display.update()
            url = "http://www.revth.com:12300/rank"
            response = requests.request("GET", url)
            rank_date_json = response.text
            rank_date_list = json.loads(rank_date_json)
            page = 0
            pygame.display.update()
            while ranking_surface:
                eventlist = pygame.event.get()
                for event in eventlist:
                    if event.type == pygame.QUIT:
                        Endgame()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if lastpage_button.mousepress(event.pos):
                            if page > 0:
                                page -= 1
                        elif nextpage_button.mousepress(event.pos):
                            if (page+1)*7 <= len(rank_date_list):
                                page += 1
                        elif return_button.mousepress(event.pos):
                            ranking_surface = False
                            home_surface = True
                            break
                window.blit(backsurface,(0,0))
                lastpage_button.draw(window)
                nextpage_button.draw(window)
                return_button.draw(window)
                window.blit(title_surface,(200,300))
                for i in range(1,8):
                    rank = rankfont.render(str(i+page*7),True,BLACKE)
                    window.blit(rank,(220,int(320+i*32)))
                    pygame.display.update()
                for i in range(0,7):
                    id = Text_ID(250,30,420,int(308+(i+1)*32),rank_date_list[i+page*7]['name'])
                    id.draw(window)
                    pygame.display.update()
                for i in range(0,7):
                    score = rankfont.render(str(rank_date_list[i+page*7]['score']),True,BLACKE)
                    window.blit(score,(700,int(320+(i+1)*32)))
                    pygame.display.update()
        elif history_surface: #历史战绩界面
            backsurface = pygame.image.load("background.jpg")
            window.blit(backsurface,(0,0))
            titlefont = pygame.font.Font('fdbsjw.ttf',40)
            title_surface = titlefont.render("ID           时间                分数",True,BLACKE)
            rankfont = pygame.font.Font("fdbsjw.ttf",20)
            lastpage_button = button(94,37,900,400,"上一页")
            nextpage_button = button(94,37,900,460,'下一页')
            lastpage_button.draw(window)
            nextpage_button.draw(window)
            return_button = button(63,37,0,0,"返回")
            return_button.draw(window)
            pygame.display.update()
            page = 0
            pygame.display.update()
            while history_surface:
                eventlist = pygame.event.get()
                for event in eventlist:
                    if event.type == pygame.QUIT:
                        Endgame()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if lastpage_button.mousepress(event.pos):
                            if page > 0:
                                page -= 1
                        elif nextpage_button.mousepress(event.pos):
                                page += 1
                        elif return_button.mousepress(event.pos):
                            history_surface = False
                            home_surface = True
                            break
                window.blit(backsurface,(0,0))
                lastpage_button.draw(window)
                nextpage_button.draw(window)
                return_button.draw(window)
                window.blit(title_surface,(200,300))
                response = history_date(login_class,page)
                response_data = json.loads(response.text)
                response_data = response_data['data']
                for i in range(0,7):
                    if i >= len(response_data):
                        break
                    id = Text_ID(250,30,200,int(342+i*32),str(response_data[i]['id']))
                    id.draw(window)
                    pygame.display.update()
                for i in range(0,7):
                    if i >= len(response_data):
                        break
                    time1 = rankfont.render(str(response_data[i]['timestamp']),True,BLACKE)
                    window.blit(time1,(400,int(320+(i+1)*32)))
                    pygame.display.update()
                for i in range(0,7):
                    if i >= len(response_data):
                        break
                    score = rankfont.render(str(response_data[i]['score']),True,BLACKE)
                    window.blit(score,(700,int(320+(i+1)*32)))
                    pygame.display.update()

                

def Endgame():
    exit()


class TextBox:
    def __init__(self, w, h, x, y, font=None, callback=None):
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
        self.rect = None  # 文本框矩形区域
        # 创建
        self.__surface = pygame.Surface((w, h))
        self.rect = self.__surface.get_rect()
        self.font = pygame.font.Font(None, 31)

    def draw(self, dest_surf):
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        dest_surf.blit(self.__surface, (self.x, self.y))
        dest_surf.blit(text_surf, (self.x+5, self.y + (self.height - text_surf.get_height())),
                       (0, 0, self.width-5, self.height))

    def key_down(self, event):
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
        list = [self.x, self.y, self.width, self.height]
        return list

    def gettext(self):
        return self.text


def callback():
    print("回车测试")


class background():
    def __init__(self):
        pass

    def newscreen(self):
        screen = pygame.display.set_mode([1280, 591])  # 设置窗口大小
        pygame.display.set_caption('13water')  # 设置窗口标题
        back = pygame.image.load("background.jpg")
        screen.blit(back, (0, 0))
        text1, text2 = background.Textsurface()
        screen.blit(text1, (420, 400))
        screen.blit(text2, (420, 460))
        return screen

    def Textsurface():
        pygame.font.init()
        font = pygame.font.Font("fdbsjw.ttf", 30)
        textsurface1 = font.render('用户名:', True, BLACKE)
        textsurface2 = font.render('密   码:', True, BLACKE)
        return textsurface1, textsurface2


def change(rect, userlist, passwordlist):
    x, y = rect
    global userinput
    global passwordinput
    if x > userlist[0] and x < userlist[0]+userlist[2] and y > userlist[1] and y < userlist[1]+userlist[3]:
        userinput = True
    else:
        userinput = False
    if x > passwordlist[0] and x < passwordlist[0]+passwordlist[2] and y > passwordlist[1] and y < passwordlist[1]+passwordlist[3]:
        passwordinput = True
    else:
        passwordinput = False


class button():
    def __init__(self, w, h, x, y, buttontext, font='fdbsjw.ttf'):
        """ 
        w:按钮的宽度
        h:按钮的高度
        x:按钮的x坐标
        y:按钮的y坐标
        buttontext:按钮显示的文字
        """
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font, 31)
        self.__surface = pygame.Surface((w, h))
        self.rect = self.__surface.get_rect()
        self.rect[0] = self.x
        self.rect[1] = self.y
        self.buttontext = buttontext

    def draw(self, dest_surf):
        text_surf = self.font.render(self.buttontext, True, (0, 255, 0))
        dest_surf.fill((50, 50, 255), self.rect)
        dest_surf.blit(text_surf, (self.x, self.y))

    def mousepress(self, rect):
        x, y = rect
        if x > self.x and x < self.x+self.width and y > self.y and y < self.y+self.height:
            return True
        else:
            return False


class Login(button):
    token = None
    id = None
    def __init__(self, user, password):
        self.user = user
        self.password = password
    def login(self):
        url = "http://api.revth.com/auth/login"
        payload = {"username":self.user,"password":self.password}
        headers = {"Content-Type": 'application/json'}
        payload = json.dumps(payload)
        self.response = requests.post(
             url, data=payload, headers=headers)
        print(self.response.text)
        self.response_statue_code = self.response.status_code
        response_data = json.loads(self.response.text)
        response_data = response_data['data']
        if self.response.status_code == 200:
            self.token = response_data['token']
            self.id = response_data['user_id']
    def gettoken(self):
        return self.token
    def getid(self):
        return self.id


def register(user, password):
    url='http://www.revth.com:12300/auth/register2'
    form_data={
        "username": user,
        "password": password,
        "student_number":'031702641',
        "student_password":'a15159756622'
    }
    headers={
        "Content-Type":'application/json',
    }
    response=requests.post(url=url,headers=headers,data=json.dumps(form_data),verify=False)
    print(response.text)

class Text_ID:
    def __init__(self, w, h, x, y, text):
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
        self.text = text  # 文本框内容
        self.callback = callback
        self.rect = None  # 文本框矩形区域
        # 创建
        self.__surface = pygame.Surface((w, h))
        self.rect = self.__surface.get_rect()
        self.font = pygame.font.Font('fdbsjw.ttf', 20)

    def draw(self, dest_surf):
        text_surf = self.font.render(self.text, True, BLACKE)
        dest_surf.blit(text_surf, (self.x+5, self.y + (self.height - text_surf.get_height())),(0, 0, self.width-5, self.height))
def history_date(login_class,page):
    url = "http://www.revth.com:12300/history"
    head = {'X-Auth-Token':login_class.gettoken()}
    query = {'player_id':login_class.getid(),'limit':7,'page':page}
    response = requests.get(url,headers = head,data = query)
    return response
def chupai(login_class):
    url ="http://api.revth.com/game/open"
    token1 = login_class.gettoken()
    date = {"X-Auth-Token":token1}
    # date = json.dumps(date)
    response = requests.post(url,headers = date)
    card = response.text
    card = json.loads(card)
    card = card['data']
    id = card['id']
    card = card['card']
    print(card)
    card = ai.AI(card)
    url = 'http://api.revth.com/game/submit'
    header = {
        "X-Auth-Token":token1,
        "Content-Type":"application/json"
    }
    data = {
        "id" :id,
        "card" : card
    }
    # header = json.dumps(header)
    data = json.dumps(data)
    response = requests.post(url,data = data, headers = header )
    print(response.text)
if __name__ == "__main__":
    StartGame()