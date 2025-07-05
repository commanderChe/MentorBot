import pygame, json
from random import *
class Player:
    def __init__(self, x, y, b, a, color, score, pictures):
        self.x=x
        self.y=y
        self.b=b
        self.a=a
        self.color=color
        self.score=score
        self.flag_w=False
        self.flag_s=False
        self.flag_a=False
        self.flag_d=False
        self.pictures=pictures
        self.direction=0
        self.boost=0
    def move(self, key_up, key_left, key_down, key_right, w, h, t):
        keys=pygame.key.get_pressed()
        self.flag_w=keys[key_up]
        self.flag_a=keys[key_left]
        self.flag_s=keys[key_down]
        self.flag_d=keys[key_right]
        if self.boost>0:
            boost=2
        else:
            boost=1
        if self.flag_w==True:
            self.y-=self.b*boost
        if self.flag_s==True:
            self.y+=self.b*boost
        if self.flag_a==True:
            self.direction=0
            self.x-=self.b*boost
        if self.flag_d==True:
            self.direction=1
            self.x+=self.b*boost
        if self.y<t:
            self.y=t
        if self.y>h-self.pictures[0].get_size()[1]:
            self.y=h-self.pictures[0].get_size()[1]
        if self.x<0:
            self.x=0
        if self.x>w-self.pictures[0].get_size()[0]:
            self.x=w-self.pictures[0].get_size()[0]
    def draw(self, screen):
        if self.a==3:
            pygame.draw.rect(screen, self.color, [self.x, self.y, self.pictures[0].get_size()[0], self.pictures[0].get_size()[1]], self.a)
        screen.blit(self.pictures[self.direction], (self.x, self.y))
class Parameters:
    def __init__(self):
        self.startscore=120
        self.logo1=pygame.image.load("Images\\RedSnailRight.png")
        self.logo2=pygame.image.load("Images\\BlueSnailLeft.png")
        self.menu=[pygame.image.load("Images\\NewGame.png"), pygame.image.load("Images\\Resume.png"), pygame.image.load("Images\\Creator.png"), pygame.image.load("Images\\Rules.png"), pygame.image.load("Images\\Exit.png")]
        self.countdown=pygame.image.load("Images\\Countdown.png")
        self.control1=pygame.image.load("Images\\Control1.png")
        self.control2=pygame.image.load("Images\\Control2.png")
        self.legend=pygame.image.load("Images\\Legend.png")
        self.actions=[pygame.image.load("Images\\Boost.png"), pygame.image.load("Images\\Tag.png"), pygame.image.load("Images\\Teleport.png"), pygame.image.load("Images\\Pass.png"), pygame.image.load("Images\\Clear.png")]
        self.player1=Player(275, 375, 1, 3, [0, 255, 0], self.startscore, [pygame.image.load("Images\\RedSnailLeft.png"), pygame.image.load("Images\\RedSnailRight.png")])
        self.player2=Player(475, 475, 1, 3, [0, 255, 0], self.startscore, [pygame.image.load("Images\\BlueSnailLeft.png"), pygame.image.load("Images\\BlueSnailRight.png")])
        self.activescreen=0
        if randint(1, 2)==1:
            self.player1.a=0
            self.player2.a=3
        else:
            self.player1.a=3
            self.player2.a=0
        self.FPS=60
        self.screen=pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        self.clock=pygame.time.Clock()
        self.h=pygame.display.Info().current_h
        self.w=pygame.display.Info().current_w
        self.my_font = pygame.font.SysFont("None", 60)
        splashtextcolor=(0, 255, 255)
        self.text3 = pygame.font.SysFont("None", 50).render("LevPass Studio presents", True, splashtextcolor)
        self.text4 = pygame.font.SysFont("None", 120).render("SNAIL'S GOTCHA", True, splashtextcolor)
        self.text5 = pygame.font.SysFont("None", 30).render("Press mouse button or any key", True, splashtextcolor)
        self.winner=pygame.font.SysFont("None", 120).render("WINNER", True, "Blue")
        self.lst=[]
        self.lst2=[]
        self.activetool=0
        self.game_run = True
        self.x=0
        self.timer_event=pygame.USEREVENT+1
        self.timer_walking=pygame.USEREVENT+2
        self.startscore=120
        self.deltascore=0.1
        self.splashcolor="Black"
        self.menucolor="White"
        self.rulescolor="White"
        self.gamecolor="PaleGreen"
        self.toolcolor="SteelBlue"
        self.scorecolor="White"
        self.toolh=120
        self.itemw=30
        self.itemh=30
        self.time=3
        self.sounds=[pygame.mixer.Sound("Sounds\\Boost.wav"), pygame.mixer.Sound("Sounds\\Tag.wav"), pygame.mixer.Sound("Sounds\\Teleport.wav")]
        self.load()
    def timerstart(self, ms):
        pygame.time.set_timer(self.timer_event, ms)
    def timerstop(self):
        self.timerstart(0)
    def walkingstart(self, ms):
        pygame.time.set_timer(self.timer_walking, ms)
    def walkingstop(self):
        self.walkingstart(0)
    def load(self):
        try:
            file=open("game.dat", "r")
            s=file.read()
            file.close()
            a=json.loads(s)
            self.lst=a["creator"]
        except:
            pass
    def save(self):
        d={"creator": self.lst}
        s=json.dumps(d, skipkeys=True, allow_nan=True, indent=4)
        file=open("game.dat", "w")
        file.write(s)
        file.close()
def SplashScreen():
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN or event.type==params.timer_event:
            params.activescreen=1
            params.timerstop()
    params.screen.fill(params.splashcolor)
    params.screen.blit(params.text3, (params.w/2-params.text3.get_size()[0]/2, params.h/4))
    params.screen.blit(params.text4, (params.w/2-params.text4.get_size()[0]/2, params.h/2))
    params.screen.blit(params.text5, (params.x, params.h*3/4))
    params.screen.blit(pygame.transform.scale_by(params.logo1, 4), ((params.w/2-params.text4.get_size()[0]/2-params.logo1.get_size()[0]*5, params.h/2-params.logo1.get_size()[1]*4+params.text4.get_size()[1])))
    params.screen.blit(pygame.transform.scale_by(params.logo2, 4), ((params.w/2+params.text4.get_size()[0]/2+params.logo2.get_size()[0], params.h/2-params.logo2.get_size()[1]*4+params.text4.get_size()[1])))
    params.x+=4
    if params.x>params.w:
        params.x=-params.text5.get_size()[0]
def MenuScreen():
    dw=params.menu[0].get_size()[0]
    dx=(params.w-dw)/2
    dh=params.menu[0].get_size()[1]
    dy=(params.h-dh*5)/6
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            params.game_run = False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if event.pos[0]>=dx and event.pos[0]<=dx+dw and event.pos[1]>=dy and event.pos[1]<=dy+dh:
                    params.activescreen=2
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Sounds\\Game.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=-1)
                    params.player1.score=params.startscore
                    params.player2.score=params.startscore
                    params.lst2=params.lst.copy()
                    params.timerstart(100)
                    params.walkingstart(20)
                elif event.pos[0]>=dx and event.pos[0]<=dx+dw and event.pos[1]>=dy*2+dh and event.pos[1]<=dy*2+dh*2:
                    params.activescreen=2
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Sounds\\Game.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=-1)
                    params.timerstart(100)
                    params.walkingstart(20)
                elif event.pos[0]>=dx and event.pos[0]<=dx+dw and event.pos[1]>=dy*3+dh*2 and event.pos[1]<=dy*3+dh*3:
                    params.activescreen=5
                elif event.pos[0]>=dx and event.pos[0]<=dx+dw and event.pos[1]>=dy*4+dh*3 and event.pos[1]<=dy*4+dh*4:
                    params.activescreen=6
                elif event.pos[0]>=dx and event.pos[0]<=dx+dw and event.pos[1]>=dy*5+dh*4 and event.pos[1]<=dy*5+dh*5:
                    params.game_run=False
    params.screen.fill(params.menucolor)
    params.screen.blit(pygame.transform.scale_by(params.logo1, 4), (params.logo1.get_size()[0], params.logo1.get_size()[1]))
    params.screen.blit(pygame.transform.scale_by(params.logo2, 4), (params.w-params.logo1.get_size()[0]*5, params.h-params.logo1.get_size()[1]*5))
    for i in range(len(params.menu)):
        if i!=3:
            params.screen.blit(params.menu[i], (dx, dy*(i+1)+dh*i))
def WinnerScreen(player):
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                params.activescreen=1
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Sounds\\Menu.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=-1)
                params.timerstop()
                params.walkingstop()
                params.lst2=params.lst.copy()
                params.player1.score=params.startscore
                params.player2.score=params.startscore
    params.screen.fill(params.rulescolor)
    params.screen.blit(pygame.transform.scale_by(player.pictures[0], 8), (params.w/2-player.pictures[0].get_size()[0]*4, params.h/2-player.pictures[0].get_size()[1]*4))
    params.screen.blit(params.winner, (params.w/2-params.winner.get_size()[0]/2, params.h/2+player.pictures[0].get_size()[1]*6))
def CreaterScreen():
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if event.pos[0]>=0 and event.pos[0]<params.itemw*6 and event.pos[1]>0 and event.pos[1]<params.itemh*2:
                    params.activetool=event.pos[0]//(params.itemw*2)
                if event.pos[0]>=params.itemw*8 and event.pos[0]<params.itemw*10 and event.pos[1]>0 and event.pos[1]<params.itemh*2:
                    params.lst.clear()
                if event.pos[1]>=params.toolh:
                    flag=True
                    for i in range(len(params.lst)-1, -1, -1):
                        if params.lst[i][1]==event.pos[0]//params.itemw and params.lst[i][2]==event.pos[1]//params.itemh:
                            flag=False
                    if flag==True:
                        params.lst.append([params.activetool, event.pos[0]//params.itemw, event.pos[1]//params.itemh])
            if event.button==3:
                if event.pos[1]>=params.toolh:
                    for i in range(len(params.lst)-1, -1, -1):
                        if params.lst[i][1]==event.pos[0]//params.itemw and params.lst[i][2]==event.pos[1]//params.itemh:
                            params.lst.pop(i)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                params.activescreen=1
                params.save()
    params.screen.fill(params.gamecolor)
    pygame.draw.rect(params.screen, params.toolcolor, [0, 0, params.w, params.toolh])
    count=0
    for item in params.actions:
        params.screen.blit(pygame.transform.scale_by(item, 2), (item.get_size()[0]*2*count, 0))
        count+=1
    params.screen.blit(params.legend, (0, params.actions[0].get_size()[1]*2))
    for item in params.lst:
        params.screen.blit(params.actions[item[0]], (item[1]*params.itemw, item[2]*params.itemh))
def MainScreen():
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                params.activescreen=1
                params.timerstop()
                params.walkingstop()
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Sounds\\Menu.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=-1)
        if event.type==params.timer_event:
            if params.player1.a>0:
                params.player1.score-=params.deltascore
                if params.player1.score<0:
                    params.activescreen=4
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Sounds\\Winner.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=-1)
            if params.player2.a>0:
                params.player2.score-=params.deltascore
                if params.player2.score<0:
                    params.activescreen=3
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Sounds\\Winner.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(loops=-1)
            if params.player1.boost>0:
                params.player1.boost-=params.deltascore
            else:
                params.player1.boost=0
            if params.player2.boost>0:
                params.player2.boost-=params.deltascore
            else:
                params.player2.boost=0
        if event.type==params.timer_walking:
            params.player1.move(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, params.w, params.h, params.toolh)
            params.player2.move(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, params.w, params.h, params.toolh)
            if ((params.player1.x - params.itemw < params.player2.x < params.player1.x + params.itemw) and (params.player1.y - params.itemh < params.player2.y < params.player1.y + params.itemh)):
                if params.player1.a==0:  
                    params.player1.a=3
                    params.player2.a=0
                    params.player1.x=randint(1, params.w)
                    params.player1.y=randint(1, params.h)
                else:
                    params.player1.a=0
                    params.player2.a=3
                    params.player2.x=randint(1, params.w)
                    params.player2.y=randint(1, params.h)
                params.sounds[1].play()
            for i in range(len(params.lst2)-1, -1, -1):
                flag=False
                if ((params.player1.x - params.itemw < params.lst2[i][1]*params.itemw < params.player1.x + params.itemw) and (params.player1.y - params.itemh < params.lst2[i][2]*params.itemh < params.player1.y + params.itemh)):
                    flag=True
                    if params.lst2[i][0]==0:
                        params.player1.boost=params.time
                        params.sounds[0].play()
                    if params.lst2[i][0]==1:
                        params.player1.a=3
                        params.player2.a=0
                        params.sounds[1].play()
                    if params.lst2[i][0]==2:
                        params.player1.x=randint(1, params.w)
                        params.player1.y=randint(1, params.h)
                        params.sounds[2].play()
                if ((params.player2.x - params.itemw < params.lst2[i][1]*params.itemw < params.player2.x + params.itemw) and (params.player2.y - params.itemh < params.lst2[i][2]*params.itemh < params.player2.y + params.itemh)):
                    flag=True
                    if params.lst2[i][0]==0:
                        params.player2.boost=params.time
                        params.sounds[0].play()
                    if params.lst2[i][0]==1:
                        params.player1.a=0
                        params.player2.a=3
                        params.sounds[1].play()
                    if params.lst2[i][0]==2:
                        params.player2.x=randint(1, params.w)
                        params.player2.y=randint(1, params.h)
                        params.sounds[2].play()
                if flag:
                    params.lst2.pop(i)
    params.screen.fill(params.gamecolor)
    pygame.draw.rect(params.screen, params.toolcolor, [0, 0, params.w, params.toolh])
    params.screen.blit(pygame.transform.scale2x(params.player1.pictures[1]), (params.itemw*2, params.itemh))
    params.screen.blit(params.control2, (params.itemw*4+params.player1.pictures[1].get_size()[0], 0))
    text = params.my_font.render(str(round(params.player1.score, 1)), True, params.scorecolor)
    params.screen.blit(text, (params.w/2-params.toolh, params.itemh*2))
    params.screen.blit(params.countdown, (params.w/2-params.toolh-params.countdown.get_size()[0], params.itemh))
    params.screen.blit(pygame.transform.scale2x(params.player2.pictures[1]), (params.itemw*2+params.w/2, params.itemh))
    params.screen.blit(params.control1, (params.itemw*4+params.w/2+params.player2.pictures[1].get_size()[0], 0))
    text = params.my_font.render(str(round(params.player2.score, 1)), True, params.scorecolor)
    params.screen.blit(text, (params.w-params.toolh, params.itemh*2))
    params.screen.blit(params.countdown, (params.w-params.toolh-params.countdown.get_size()[0], params.itemh))
    for item in params.lst2:
        params.screen.blit(params.actions[item[0]], (item[1]*params.itemw, item[2]*params.itemh))
    params.player1.draw(params.screen)
    params.player2.draw(params.screen)
def RulesScreen():
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                params.activescreen=1
    params.screen.fill(params.rulescolor)
def main():
    params.timerstart(10000)
    pygame.mixer.music.load("Sounds\\Menu.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=-1)
    while params.game_run:
        if params.activescreen==0:
            SplashScreen()
        elif params.activescreen==1:
            MenuScreen()
        elif params.activescreen==2:
            MainScreen()
        elif params.activescreen==3:
            WinnerScreen(params.player1)
        elif params.activescreen==4:
            WinnerScreen(params.player2)
        elif params.activescreen==5:
            CreaterScreen()
        pygame.display.update()
        params.clock.tick(params.FPS)
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    params=Parameters()
    main()
    pygame.quit()