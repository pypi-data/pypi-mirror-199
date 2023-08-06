import pygame as pg
import functions as f
import time

pg.init()

font = pg.font.SysFont('arial', 40)

pg.mixer.init()

def checkB(pos, posB,size):
    return True if pos[0]>posB[0] and pos[0]<posB[0]+size[0] and pos[1]>posB[1] and pos[1]<posB[1]+size[1] else False

def min(ns):
    mn = ns[0]
    for _ in ns:
        if mn > _:
            mn = _

def max(ns):
    mn = ns[0]
    for _ in ns:
        if mn < _:
            mn = _


class TextBox():
    def __init__(self,name,pos,size,napr,text,maxlen,n,font = None):
        self.name = name
        self.pos = pos
        self.size = size
        self.pos1 = (0,0)
        self.size1 = (0,0)
        self.napr = napr
        self.text = text
        self.maxlen = maxlen
        self.defa = n
        self.x1 = 0
        self.x2 = 0
        self.down = False
        self.key = None
        self.keytime = 0
        self.unic = None
        self.inFocus = False
        self.font = pg.font.SysFont('arial', size[1]-26)
        self.rtx = ''
        self.sdpos=(0,0)
        if font != None:
            self.font = font
    
    def update(self,e):
        if e.type==pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                p = e.pos
                p = (p[0]-self.sdpos[0],p[1]-self.sdpos[1])
                if checkB(p,self.pos1,self.size1):
                    self.inFocus = True
                    pg.key.start_text_input()
                else:
                    self.inFocus = False
        elif e.type == pg.KEYDOWN:
            if self.inFocus:
                self.down = True
                self.key = e.key
                self.unic = e.unicode
        elif e.type == pg.KEYUP:
            self.down = False
    
    def render(self,surf):
        if self.down:
            if time.time() - self.keytime > 0.11:
                if self.key == pg.K_RETURN:
                    self.defa(self.text)
                    self.text = ''
                    pg.key.stop_text_input()
                    self.inFocus = False
                elif self.key == pg.K_BACKSPACE:
                    self.text = self.text[:len(self.text)-1]
                else:
                    self.text+=self.unic
                self.keytime = time.time()
        self.rtx = self.text if self.text != '' else self.name
        self.x1 = 0
        if self.napr == 'right':
            self.x2 = len(self.rtx)
            lentx = self.font.render(self.rtx,1,(255,255,255)).get_rect()[2]
            self.pos1 = self.pos
            if lentx < self.size[0]:
                self.size1 = self.size
            elif lentx > self.maxlen:
                self.size1 = (self.maxlen,self.size[1])
                while self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255)).get_rect()[2] > self.maxlen-30:
                    self.x1 += 6
            else:
                self.size1 = (self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255)).get_rect()[2]+40, self.size[1])
                
        else:
            lentx = self.font.render(self.rtx,1,(255,255,255)).get_rect()[2]
            self.x2 = len(self.rtx)
            if lentx < self.size[0]:
                self.size1 = self.size
            elif lentx > self.maxlen:
                self.size1 = (self.maxlen,self.size[1])
                while self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255)).get_rect()[2] > self.maxlen-30:
                    self.x1 += 6
            else:
                self.size1 = (self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255)).get_rect()[2]+40, self.size[1])
            self.pos1 = (self.pos[0] - self.size1[0]-100,self.pos[1])
        
        
        surfacea = pg.Surface(self.size1)
        pg.draw.rect(surfacea,(20,20,10),((0,0),self.size1))
        surfacea.set_alpha(150)
        surf.blit(surfacea,(self.pos1))
        pg.draw.rect(surf,(255,255,255),(self.pos1,self.size1),4)
        rtxb = self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255))
        surf.blit(rtxb,(self.pos1[0]+20,self.pos1[1]+(self.size[1]-26)//2))
            

class Buttons():
    def __init__(self, pos, size, colors, type, text, defa, font=None, sound=None, img1=None, img2=None):
        self.pos = pos
        self.size = size
        self.sdpos=(0,0)
        self.type = type
        self.text = text
        self.defa = defa
        self.colors = colors
        self.img1 = img1
        self.img2 = img2
        self.img = img1
        self.sound = sound
        self.n = 0
        self.draw = True if img1 != None and img2 != None else False
        self.mpos = (0,0)
        self.click = False
        self.clb = 0
        self.font = pg.font.SysFont('arial', int(size[1]-26))
        self.clickg = 0
        self.on = False
        if font != None:
            self.font = font
    
    def update(self,e):
        if e.type == pg.MOUSEBUTTONDOWN:
            self.clickg = e.button
            if e.button == 1:
                self.clb = 0
                self.mpos = e.pos
                self.mpos = (self.mpos[0]-self.sdpos[0],self.mpos[1]-self.sdpos[1])
                if checkB(self.mpos,self.pos,self.size):
                    self.click = True
                    if self.sound != None:
                        self.sound.play()
                else:
                    self.click = False
        elif e.type == pg.MOUSEBUTTONUP:
            self.clickg = 0
            if self.click:
                self.clb = 1
                self.click = False
                if checkB(self.mpos,self.pos,self.size):
                    if self.type == 'click':
                        self.defa()
                    if self.type == 'switch':
                        self.on = True
                        self.defa()
                    if self.type == 'switch+':
                        self.on = not(self.on)
                        self.defa()
        elif e.type == pg.MOUSEMOTION:
            self.mpos = e.pos
            self.mpos = (self.mpos[0]-self.sdpos[0],self.mpos[1]-self.sdpos[1])
            if checkB(self.mpos,self.pos,self.size):
                if self.clb == 1:
                    if self.sound != None:
                        self.sound.play()
                        self.clb = 2
                if self.clb == 0:
                    self.clb = 1
                if self.clickg == 1:
                    self.click = True
            else:
                self.click = False
                self.clb = 0
    
    def render(self,surf):
        if self.click:
            if self.type == 'press':
                self.defa()
        if self.clb == 1:
            self.n = 1
            self.img = self.img2
        elif self.clb == 0:
            self.n = 0
            self.img = self.img1
        if self.type=='switch' or self.type == 'switch+':
            if self.on or self.clb != 0:
                self.n = 1
                self.img = self.img2
            else:
                self.n = 0
                self.img = self.img1
            
        o = (255,255,255) if self.colors[self.n][0] < 100 and self.colors[self.n][1] > 100 and self.colors[self.n][2] < 100 else (255,255,255) if self.colors[self.n][0] < 100 and self.colors[self.n][1] < 100 and self.colors[self.n][2] < 100 else (0,0,0)
            
        pg.draw.rect(surf, (self.colors[self.n]),(self.pos,self.size))
        pg.draw.rect(surf, o,(self.pos,self.size),2)
        if self.draw:
            surf.blit(self.img,(self.pos[0]+4, self.pos[1]+4))
            
        if self.text != '' and self.text != None:
            try:
                n = self.font.render(self.text,1,o)
            except:
                f = pg.font.SysFont('arial', int(self.size[1]-40))
            surf.blit(n,((self.pos[0]+self.size[0]//2)-(n.get_rect()[2]//2)-6,(self.pos[1]+self.size[1]//2)-n.get_rect()[3]//2))


class Slider():
    def __init__(self,pos,size,colors,n,input,font = None):
        self.pos = pos
        self.size = size
        self.sdpos=(0,0)
        self.colors = colors
        self.znach = range(n[0],n[1],n[2])
        self.perspos = self.size[0]/len(self.znach)
        self.input = input
        self.n = 1
        self.click = False
        self.i = 0
        self.click = False
        self.font = font if font != None else pg.font.SysFont('arial',int(size[1]//1.8))
    
    def update(self,e):
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                pos = e.pos
                pos = (pos[0]-self.sdpos[0],pos[1]-self.sdpos[1])
                if checkB(pos,self.pos,self.size):
                    self.click=True
                    for i in range(len(self.znach)):
                        if pos[0] > self.perspos*i+self.pos[0] and pos[0] < self.perspos*(i+1)+self.pos[0]:
                            self.input = self.znach[i]

        if e.type == pg.MOUSEMOTION and self.click:
            pos = e.pos
            pos = (pos[0]-self.sdpos[0],pos[1]-self.sdpos[1])
            if checkB(pos,self.pos,self.size):
                for i in range(len(self.znach)):
                    if pos[0] > self.perspos*i+self.pos[0] and pos[0] < self.perspos*(i+1)+self.pos[0]:
                        self.input = self.znach[i]
        if e.type == pg.MOUSEBUTTONUP:
            self.click = False
    
    def render(self,surf):
            self.i = self.znach.index(self.input)
            s = self.font.render(str(self.input),1,(20,20,20))
            x = s.get_rect()[2]
            pg.draw.rect(surf,self.colors[0],((self.pos[0],self.pos[1] + self.size[1]*0.2),(self.size[0]+60,self.size[1]*0.60)))
            pg.draw.rect(surf,self.colors[self.n],((self.pos[0] + self.i*self.perspos+self.perspos//2-x//2,self.pos[1]),(x+20,self.size[1])))
            surf.blit(s,(self.pos[0] + self.i*self.perspos+self.perspos//2-x//2+10,self.pos[1]*1.05))


class gHotbar():
    def __init__(self,pos,num,ac,img1,img2,imgItems,numbers,rotMouse=False, font = None):
        self.rotM = rotMouse
        self.pos = pos
        self.sdpos=(0,0)
        self.num = num
        self.active = ac
        self.img1 = img1
        self.img2 = img2
        self.x = img1.get_rect()[2]
        self.y = img1.get_rect()[3]
        self.imgs = imgItems
        self.numbers = numbers
        self.font = font if font != None else pg.font.SysFont('arial', self.y-40)
    
    def update(self,e):
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                p = e.pos
                p = (p[0]-self.sdpos[0],p[1]-self.sdpos[1])
                if checkB(p,self.pos,(self.x * self.num,self.y)):
                    for i in range(self.num):
                        if e.pos[0] > self.pos[0]+self.x*i and e.pos[0] < self.pos[0]+self.x*(i+1):
                            self.active = i
            if self.rotM:
                if e.button == 5:
                    self.active += 1
                    if self.active > self.num-1:
                        self.active = 0
                elif e.button == 4:
                    self.active += -1
                    if self.active < 0:
                        self.active = self.num-1
     
    def render(self,surf):
        for i in range(self.num):
            if i == self.active:
                surf.blit(self.img2,(self.pos[0]+self.x*i, self.pos[1]))
            else:
                surf.blit(self.img1,(self.pos[0]+self.x*i, self.pos[1]))
            if self.imgs[i] != None:
                surf.blit(self.imgs[i],(self.pos[0]+self.x*i+self.x//2-self.imgs[i].get_rect()[2]//2, self.pos[1]+self.y//2-self.imgs[i].get_rect()[3]//2))
            if self.numbers[i] != 1:
                n = self.font.render(str(self.numbers[i]),1,(255,255,255))
                surf.blit(n,(self.pos[0]+self.x*(i+1)-20-n.get_rect()[2], self.pos[1]+self.y-4-n.get_rect()[3]))

class Rect():
    def __init__(self,color,pos,size,r=-1):
        self.c = color
        self.p = pos
        self.s = size
        self.r = r
    
    def render(self,surf):
        pg.draw.rect(surf,self.c,(self.p,self.s),self.r)

class Circle():
    def __init__(self,color,pos,r,r1):
        self.c = color
        self.p = pos
        self.r = r
        self.r1 = r1
    
    def render(self,surf):
        pg.draw.circle(surf,self.c,self.p,self.r,self.r1)

class label():
    def __init__(self,pos,text,c=None,s=24,font = None):
        self.text = text.split('\n')
        self.pos = pos
        self.c = (255,255,255) if c == None else  c
        self.font = font if font != None else pg.font.SysFont('arial',s)
    
    def render(self,surf):
        self.col = 0
        for l in self.text:
            s = self.font.render(l, 1, self.c)
            surf.blit(s, (self.pos[0], self.pos[1]+self.col))
            self.col+=s.get_height()+6

class Img():
    def __init__(self,img,pos):
        self.img = img
        self.pos = pos
    
    def render(self, surf):
        surf.blit(self.img, self.pos)

class BoxWithWG():
    def __init__(self,pos,size,colors, type, defa = None, sound = None):
        self.data = {}
        self.p = pos
        self.s = size
        self.cs = colors
        self.cl = False
        self.defa = defa
        self.sound = sound
        self.WGs = []
        self.type = type
        self.blocked = False
        self.click = False
        self.coefsw = [0, 0]
        self.on = 0
        self.ups = ("<class 'pgWitgets.Buttons'>", "<class 'pgWitgets.TextBox'>", "<class 'pgWitgets.Slider'>","<class '__main__.Buttons'>", "<class '__main__.TextBox'>", "<class '__main__.Slider'>")
    
    def add(self,obj):
        self.WGs.append(obj)
    
    def update(self,e):
        if self.type == 1:
            for _ in self.WGs:
                if str(type(_)) in self.ups:
                    if str(type(_)) in ("<class 'pgWitgets.Buttons'>","<class '__main__.Buttons'>"):
                        if self.blocked:
                            _.click = False
                    _.sdpos=self.p
                    _.update(e)
        else:
            if e.type == pg.MOUSEBUTTONDOWN:
                self.mpos = f.sumM([list(e.pos), self.coefsw])
                if e.button == 1:
                    if checkB(self.mpos,self.p,self.s):
                        self.click = True
                        self.on = 0
                        if self.sound != None:
                            pass
                            self.sound.play()
            elif e.type == pg.MOUSEBUTTONUP:
                if self.click:
                    self.on = 1
                    self.click = False
                self.mpos = f.sumM([list(e.pos), self.coefsw])
                if checkB(self.mpos,self.p,self.s):
                    if self.defa != None:
                        if not(self.blocked):
                            self.defa(self, self.data)
                        self.blocked = False
            elif e.type == pg.MOUSEMOTION:
                self.mpos = f.sumM([list(e.pos), self.coefsw])
                if checkB(self.mpos,self.p,self.s):
                    if not(self.on):
                        if self.sound != None:
                            pass
                            self.sound.play()
                    self.click = True
                    self.on = 1
                else:
                    self.click = False
                    self.on = 0
    
    def render(self,surf,pos = None):
        pos = self.p if pos == None else pos
        s = pg.Surface(self.s)
        s.fill(self.cs[self.on])
        for _ in self.WGs:
            _.render(s)
        surf.blit(s,(pos))
        
        
class Swip():
    def __init__(self, pos, size, color, borders):
        self.p = pos
        self.s = size
        self.sw = 0
        self.tab = False
        self.borders = borders
        self.swiped = False
        self.c = color
        self.bs = []
        self.mpos = [0, 0]
    
    def add(self,obj):
        self.bs.append(obj)
    
    def update(self, e):
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                p = e.pos
                if checkB(p,self.p,self.s):
                    self.tab = True
            if e.button == 4:
                self.swiped = False
                self.sw += 50
            if e.button == 5:
                self.swiped = False
                self.sw -= 50
            
        elif e.type == pg.MOUSEBUTTONUP:
            self.tab = False
            self.swiped = False
        
        elif e.type == pg.MOUSEMOTION:
            p = e.pos
            self.mpos = p
            self.swiped = True
            if self.tab:
                self.sw += e.rel[1]
        self.sw = self.borders[0] if self.sw < self.borders[0] else self.sw
        self.sw = self.borders[1] if self.sw > self.borders[1] else self.sw
        if checkB(self.mpos, self.p, self.s):
            for _ in self.bs:
                if self.swiped:
                    _.blocked = True
                _.coefsw = [-self.p[0], -self.sw - self.p[1]]
                _.update(e)
            
    def render(self,surf):
        s = pg.Surface(self.s)
        s.fill(self.c)
        for _ in self.bs:
            _.render(s, (_.p[0], _.p[1]+self.sw))
        surf.blit(s,self.p)
        
if __name__ == "__main__":
    import random

    surf = pg.display.set_mode((2000, 1000))

    bgC = [0,0,0]
    
    def f1():
        global bgC
        bgC = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    b1 = Buttons((40, 40), (200, 40), ((40, 40, 40), (40, 250, 40)), 'click', 'click for magic', f1)

    while True:
        surf.fill(bgC)
        
        for e in pg.event.get():
            b1.update(e)

        b1.render(surf)

        pg.display.update()

















        
