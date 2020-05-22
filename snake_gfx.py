#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import pygame
import random
import time

# stale:
BLACK = (0,0,0)
WHITE = (0xff, 0xff, 0xff)
MARG = 5
MARGT = 30
SNWIDTH = 10

# opcje:
size = (700, 500) # rozmiar okna
borders = False
blocks = True
accel = False

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake") # tytul okna
kompInactive = pygame.image.load("grafika/kompInactive.png")
kompActive = pygame.image.load("grafika/kompActive.png")
grajInactive = pygame.image.load("grafika/grajInactive.png")
grajActive = pygame.image.load("grafika/grajActive.png")
multiActive = pygame.image.load("grafika/multiActive.png")
multiInactive = pygame.image.load("grafika/multiInactive.png")
przeszkodyActive = pygame.image.load("grafika/przeszkodyActive.png")
przeszkodyInactive = pygame.image.load("grafika/przeszkodyInactive.png")
aActive = pygame.image.load("grafika/aActive.png")
aInactive = pygame.image.load("grafika/aInactive.png")
krActive = pygame.image.load("grafika/krActive.png")
krInactive = pygame.image.load("grafika/krInactive.png")
head0 = [pygame.image.load("grafika/head0.png"), pygame.image.load("grafika/head0Or.png")]
head1 = [pygame.image.load("grafika/head1.png"), pygame.image.load("grafika/head1Or.png")]
head2 = [pygame.image.load("grafika/head2.png"), pygame.image.load("grafika/head2Or.png")]
head3 = [pygame.image.load("grafika/head3.png"), pygame.image.load("grafika/head3Or.png")]
main0 = [pygame.image.load("grafika/main0.png"), pygame.image.load("grafika/main0Or.png")]
main1 = [pygame.image.load("grafika/main1.png"), pygame.image.load("grafika/main1Or.png")]
tail0 = [pygame.image.load("grafika/tail0.png"), pygame.image.load("grafika/tail0Or.png")]
tail1 = [pygame.image.load("grafika/tail1.png"), pygame.image.load("grafika/tail1Or.png")]
tail2 = [pygame.image.load("grafika/tail2.png"), pygame.image.load("grafika/tail2Or.png")]
tail3 = [pygame.image.load("grafika/tail3.png"), pygame.image.load("grafika/tail3Or.png")]
turn1 = [pygame.image.load("grafika/turn1.png"), pygame.image.load("grafika/turn1Or.png")]
turn2 = [pygame.image.load("grafika/turn2.png"), pygame.image.load("grafika/turn2Or.png")]
turn3 = [pygame.image.load("grafika/turn3.png"), pygame.image.load("grafika/turn3Or.png")]
turn4 = [pygame.image.load("grafika/turn4.png"), pygame.image.load("grafika/turn4Or.png")]

for i in range(0,2):
    head0[i].set_colorkey(BLACK)
    head1[i].set_colorkey(BLACK)
    head2[i].set_colorkey(BLACK)
    head3[i].set_colorkey(BLACK)
    tail0[i].set_colorkey(BLACK)
    tail1[i].set_colorkey(BLACK)
    tail2[i].set_colorkey(BLACK)
    tail3[i].set_colorkey(BLACK)
    turn1[i].set_colorkey(BLACK)
    turn2[i].set_colorkey(BLACK)
    turn3[i].set_colorkey(BLACK)
    turn4[i].set_colorkey(BLACK)

class SnPart (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([2, 2])        
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 2
        self.rect.y = 2
    def update(self, x, y, width, height):
        self.image = pygame.Surface([width, height])        
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("grafika/point.png")
        self.rect = self.image.get_rect()
        self.rect.x = x - SNWIDTH//2
        self.rect.y = y - SNWIDTH//2
        
class Block (pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width*SNWIDTH, height*SNWIDTH])        
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def rysujWeza(x, y, head, screen, color, parts): # color=0 -> zielony, color=1 -> pomaranczowy
# 'x' i 'y' bez korekty # 0N, 1E, 2S, 3W
# head(SnPart)
# screen(lista SnPartow)
# parts jest lista list [dlug, kier]
    tailIncompl = False
    # korekty x i y
    x -= SNWIDTH//2
    y -= SNWIDTH//2
    x %= size[0]
    y %= size[1]
    lenMinusWidth = parts[0][0]-2*SNWIDTH
    scrList = []
    if(lenMinusWidth<0):
        lenMinusWidth = 0
    headLen = parts[0][0]-SNWIDTH-lenMinusWidth
    if(headLen > 0):
        if(parts[0][1] == 0):
            if y>size[1]-headLen:
                scrList.append(SnPart())
                head.update(x, y, SNWIDTH, size[1]-y) # gorna cześć heada
                head.image.blit(head0[color], (0, 0))
                scrList[0].update(x, 0, SNWIDTH, headLen-size[1]+y) # dolna cześć heada
                scrList[0].image.blit(head0[color], (0, y-size[1]))
            else:
                head.update(x, y, SNWIDTH, headLen)
                head.image.blit(head0[color], (0, 0))
        elif(parts[0][1] == 1):
            x += SNWIDTH-headLen
            if x>size[0]-headLen:
                scrList.append(SnPart())
                scrList[0].update(x, y, size[0]-x, SNWIDTH) # lewa cześć heada
                scrList[0].image.blit(head1[color], (0, 0))
                head.update(0, y, headLen-size[0]+x, SNWIDTH) # prawa cześć heada
                head.image.blit(head1[color], (x-size[0], 0))
            else:
                head.update(x, y, headLen, SNWIDTH)
                head.image.blit(head1[color], (0, 0))
        elif(parts[0][1] == 2):
            y += SNWIDTH-headLen
            if y>size[1]-headLen:
                scrList.append(SnPart())
                scrList[0].update(x, y, SNWIDTH, size[1]-y) # gorna cześć heada
                scrList[0].image.blit(head2[color], (0, 0))
                head.update(x, 0, SNWIDTH, headLen-size[1]+y) # dolna cześć heada
                head.image.blit(head2[color], (0, y-size[1]))
            else:
                head.update(x, y, SNWIDTH, headLen)
                head.image.blit(head2[color], (0, 0))
        else:
            if x>size[0]-headLen:
                scrList.append(SnPart())
                head.update(x, y, size[0]-x, SNWIDTH) # lewa cześć heada
                head.image.blit(head3[color], (0, 0))
                scrList[0].update(0, y, headLen-size[0]+x, SNWIDTH) # prawa cześć heada
                scrList[0].image.blit(head3[color], (x-size[0], 0))
            else:
                head.update(x, y, headLen, SNWIDTH)
                head.image.blit(head3[color], (0, 0))
        
    for i in range(0, len(parts)):
        lenMinusWidth = parts[i][0]-2*SNWIDTH # zeby do graficznego zmiescic skret
        if(lenMinusWidth < 0):
            lenMinusWidth = 0
        tailLen = parts[i][0]-headLen-lenMinusWidth
        if(parts[i][1] == 0): #glowny
            y += headLen
            y %= size[1]
            if y+lenMinusWidth+tailLen<size[1]:
                screen[i].update(x, y, SNWIDTH, lenMinusWidth+tailLen) # jeżeli jest skret, to i tak tailLen = 10
                if(lenMinusWidth>0):
                    for j in range(0, lenMinusWidth):
                        screen[i].image.blit(main0[color], (0, j))
            else: # jeżeli sie nie miesci
                tailIncompl = True
                screen[i].update(x, y, SNWIDTH, size[1]-y) # jeżeli jest skret, to i tak tailLen = 10
                scrList.append(SnPart())
                scrList[-1].update(x, 0, SNWIDTH, lenMinusWidth+tailLen-size[1]+y)
                if y+lenMinusWidth<size[1]:
                    for j in range(0, lenMinusWidth):
                        screen[i].image.blit(main0[color], (0, j))
                else:
                    for j in range(0, size[1]-y):
                        screen[i].image.blit(main0[color], (0, j))
                    for j in range(0, tailLen+lenMinusWidth-size[1]+y):
                        scrList[-1].image.blit(main0[color], (0, j))
            y += lenMinusWidth
            y %= size[1]
        elif(parts[i][1] == 1):
            x -= lenMinusWidth+tailLen
            x %= size[0]
            if x+lenMinusWidth+tailLen<size[0]:
                screen[i].update(x, y, lenMinusWidth+tailLen, SNWIDTH)
                if(lenMinusWidth>0):
                    for j in range(0, lenMinusWidth):
                        screen[i].image.blit(main1[color], (tailLen+j, 0))
            else: # jeżeli sie nie miesci
                screen[i].update(x, y, size[0]-x, SNWIDTH) # jeżeli jest skret, to i tak tailLen = 10
                scrList.append(SnPart())
                scrList[-1].update(0, y, lenMinusWidth+tailLen-size[0]+x, SNWIDTH)
                if x+tailLen<size[0]:
                    for j in range(tailLen, lenMinusWidth+tailLen):
                        screen[i].image.blit(main1[color], (j, 0))
                    for j in range(0, lenMinusWidth+tailLen-size[0]+x):
                        scrList[-1].image.blit(main1[color], (j, 0))
                else:
                    tailIncompl = True
                    for j in range(tailLen-size[0]+x, lenMinusWidth+tailLen-size[0]+x):
                        scrList[-1].image.blit(main1[color], (j, 0))
        elif(parts[i][1] == 2):
            y -= lenMinusWidth+tailLen
            y %= size[1]
            if y+lenMinusWidth+tailLen<size[1]:
                screen[i].update(x, y, SNWIDTH, lenMinusWidth+tailLen)
                if(lenMinusWidth>0):
                    for j in range(0, lenMinusWidth):
                        screen[i].image.blit(main0[color], (0, tailLen+j))
            else:
                screen[i].update(x, y, SNWIDTH, size[1]-y) # jeżeli jest skret, to i tak tailLen = 10
                scrList.append(SnPart())
                scrList[-1].update(x, 0, SNWIDTH, lenMinusWidth+tailLen-size[1]+y)
                if y+tailLen<size[1]:
                    for j in range(tailLen, lenMinusWidth+tailLen):
                        screen[i].image.blit(main0[color], (0, j))
                    for j in range(0, lenMinusWidth-size[1]+y+tailLen):
                        scrList[-1].image.blit(main0[color], (0, j))
                else:
                    tailIncompl = True
                    for j in range(tailLen-size[1]+y, tailLen+lenMinusWidth-size[1]+y):
                        scrList[-1].image.blit(main0[color], (0, j))
        else:
            x += headLen
            x %= size[0]
            if x+lenMinusWidth+tailLen<size[0]:
                screen[i].update(x, y, lenMinusWidth+tailLen, SNWIDTH)
                if(lenMinusWidth>0):
                    for j in range(0, lenMinusWidth):
                        screen[i].image.blit(main1[color], (j, 0))
            else: # jeżeli sie nie miesci
                tailIncompl = True
                screen[i].update(x, y, size[0]-x, SNWIDTH) # jeżeli jest skret, to i tak tailLen = 10
                scrList.append(SnPart())
                scrList[-1].update(0, y, lenMinusWidth+tailLen-size[0]+x, SNWIDTH)
                if x+lenMinusWidth<size[0]:
                    for j in range(0, lenMinusWidth):
                        screen[i].image.blit(main1[color], (j, 0))
                else:
                    for j in range(0, size[0]-x):
                        screen[i].image.blit(main1[color], (j, 0))
                    for j in range(0, lenMinusWidth-size[0]+x):
                        scrList[-1].image.blit(main1[color], (j, 0))
            x += lenMinusWidth
            x %= size[0]
        if(i == len(parts)-1): # ogon
            if(parts[i][1] == 0):
                screen[i].image.blit(tail0[color], (0, lenMinusWidth))
                if tailIncompl:
                    scrList[-1].image.blit(tail0[color], (0, scrList[-1].image.get_height()-tailLen))
            elif(parts[i][1] == 1):
                screen[i].image.blit(tail1[color], (0, 0))
                if tailIncompl:
                    scrList[-1].image.blit(tail1[color], (x-size[0], 0))
            elif(parts[i][1] == 2):
                screen[i].image.blit(tail2[color], (0, 0))
                if tailIncompl:
                    scrList[-1].image.blit(tail2[color], (0, y-size[1]))
            else:
                screen[i].image.blit(tail3[color], (lenMinusWidth, 0))
                if tailIncompl:
                    scrList[-1].image.blit(tail3[color], (scrList[-1].image.get_width()-tailLen, 0))
        else: # skret
            if(parts[i][1] == 0):
                if(parts[i+1][1] == 1):
                    screen[i].image.blit(turn1[color], (0, lenMinusWidth))
                    if tailIncompl:
                        scrList[-1].image.blit(turn1[color], (0, scrList[-1].image.get_height()-tailLen))
                else:
                    screen[i].image.blit(turn2[color], (0, lenMinusWidth))
                    if tailIncompl:
                        scrList[-1].image.blit(turn2[color], (0, scrList[-1].image.get_height()-tailLen))
            elif(parts[i][1] == 1):
                if(parts[i+1][1] == 0):
                    screen[i].image.blit(turn3[color], (0, 0))
                    if tailIncompl:
                        scrList[-1].image.blit(turn3[color], (0, 0))
                else:
                    screen[i].image.blit(turn2[color], (0, 0))
                    if tailIncompl:
                        scrList[-1].image.blit(turn2[color], (0, 0))
            elif(parts[i][1] == 2):
                if(parts[i+1][1] == 1):
                    screen[i].image.blit(turn4[color], (0, 0))
                    if tailIncompl:
                        scrList[-1].image.blit(turn4[color], (0, 0))
                else:
                    screen[i].image.blit(turn3[color], (0, 0))
                    if tailIncompl:
                        scrList[-1].image.blit(turn3[color], (0, 0))
            else:
                if(parts[i+1][1] == 0):
                    screen[i].image.blit(turn4[color], (lenMinusWidth, 0))
                    if tailIncompl:
                        scrList[-1].image.blit(turn4[color], (scrList[-1].image.get_width()-tailLen, 0))
                else:
                    screen[i].image.blit(turn1[color], (lenMinusWidth, 0))
                    if tailIncompl:
                        scrList[-1].image.blit(turn1[color], (scrList[-1].image.get_width()-tailLen, 0))
        headLen = SNWIDTH
        tailIncompl = False
    return scrList

# poczatek programu
mouse = (0, 0)
mouseLeft = False
mouseClicked = False
    
menu = True
gra = False
graKomp = False
multi = False
done = False

font = pygame.font.Font(None, 24)
font14 = pygame.font.Font(None, 14)
clock = pygame.time.Clock()
width = size[0]-2*MARG
height = size[1]-2*MARG
x = [size[0]//2//SNWIDTH*SNWIDTH+5, 105]
y = [size[1]//2//SNWIDTH*SNWIDTH+5, 55]
poz = [ [[50, 0]], [[50, 1]] ]
kier = [0, 1]
posDir = [False]*4
v = [1, 1]
vx = [0, v[1]]
vy = [-v[0], 0]
xPl = []
yPl = []
xComp = []
yComp = []
xPt = -1
yPt = -1
objectList = pygame.sprite.Group()
tmpList = pygame.sprite.Group()
random.seed()
pointed = True
point = None
score = [0, 0]
prevScore = [0, 0]
scoreText = None
waz = [ [SnPart()], [SnPart()] ]
scrList = [ [], [] ]
tmpScrList = [ [], [] ]
head = [SnPart(), SnPart()]
objectList.add(waz[0])
objectList.add(waz[1])
for i in range(0, 2):
    rysujWeza(x[i], y[i], head[i], waz[i], i, poz[i])
for w in waz:
    for part in w:
        tmpList.add(part)
tmpList.add(head[0])
tmpList.add(head[1])
tmp = Block(1, 23, random.randrange(0, 61)*10+10, random.randrange(1, 44)*10)
while pygame.sprite.spritecollideany(tmp, tmpList) != None or tmp.rect.x<MARG or tmp.rect.y<MARGT or tmp.rect.right>size[0]-MARG or tmp.rect.bottom>size[1]-MARG:
    tmp = Block(1, 23, random.randrange(0, 61)*10+10, random.randrange(1, 44)*10)
tmpBlockList = []
tmpBlockList.append(tmp)
objectList.add(tmp)
tmpList.add(tmp)
tmp = Block(37, 1, random.randrange(0, 61)*10+10, random.randrange(1, 44)*10)
while pygame.sprite.spritecollideany(tmp, tmpList) != None or tmp.rect.x<MARG or tmp.rect.y<MARGT or tmp.rect.right>size[0]-MARG or tmp.rect.bottom>size[1]-MARG:
    tmp = Block(37, 1, random.randrange(0, 61)*10+10, random.randrange(1, 44)*10)
tmpBlockList.append(tmp)
blockList = tmpBlockList
objectList.add(tmp)
tmpList.add(tmp)
lengthen = [0, 0]
przegr = [False, False]
zablok = [[], []]
end = False
    
def sprawdz0():
    for i in range(0, len(xPl)-1):
        if(yPl[i]-yPl[i+1] == 0):
            war = x[1]>=min(xPl[i],xPl[i+1]) and x[1]<=max(xPl[i],xPl[i+1])
            if(y[1]-yPl[i]<15 and y[1]-yPl[i]>0 and war):
                return False
    for i in range(0, len(xComp)-1):
        if(yComp[i]-yComp[i+1] == 0):
            war = x[1]>=min(xComp[i],xComp[i+1]) and x[1]<=max(xComp[i],xComp[i+1])
            if(y[1]-yComp[i]<15 and y[1]-yComp[i]>0 and war):
                return False
    if borders:
        if y[1]<47:
            return False
    if xPl[len(xPl)-1] == x[1] and y[1]-yPl[len(yPl)-1]<12 and y[1]-yPl[len(yPl)-1]>0:
        return False
    if xComp[len(xComp)-1] == x[1] and y[1]-yComp[len(yComp)-1]<12 and y[1]-yComp[len(yComp)-1]>0:
        return False
    if x[0] == x[1] and y[1]-y[0]<12 and y[1]-y[0]>0:
        return False
    for block in blockList:
        if x[1]>block.rect.left and x[1]<block.rect.right and y[1]-block.rect.bottom>0 and y[1]-block.rect.bottom<10:
            return False
    return True
            
def sprawdz2():
    for i in range(0, len(xPl)-1):
        if(yPl[i]-yPl[i+1] == 0):
            war = x[1]>=min(xPl[i],xPl[i+1]) and x[1]<=max(xPl[i],xPl[i+1])
            if(yPl[i]-y[1]<15 and yPl[i]-y[1]>0 and war):
                return False
    for i in range(0, len(xComp)-1):
        if(yComp[i]-yComp[i+1] == 0):
            war = x[1]>=min(xComp[i],xComp[i+1]) and x[1]<=max(xComp[i],xComp[i+1])
            if(yComp[i]-y[1]<15 and yComp[i]-y[1]>0 and war):
                return False
    if borders:
        if y[1]>size[1]-23:
            return False
    if xPl[len(xPl)-1] == x[1] and yPl[len(yPl)-1]-y[1]<12 and yPl[len(yPl)-1]-y[1]>0:
        return False
    if xComp[len(xComp)-1] == x[1] and yComp[len(yComp)-1]-y[1]<12 and yComp[len(yComp)-1]-y[1]>0:
        return False
    if x[0] == x[1] and y[0]-y[1]<12 and y[0]-y[1]>0:
        return False
    for block in blockList:
        if x[1]>block.rect.left and x[1]<block.rect.right and block.rect.top-y[1]>0 and block.rect.top-y[1]<10:
            return False
    return True
            
def sprawdz3():
    for i in range(0, len(xPl)-1):
        if(xPl[i]-xPl[i+1] == 0):
            war = y[1]>=min(yPl[i],yPl[i+1]) and y[1]<=max(yPl[i],yPl[i+1])
            if(x[1]-xPl[i]<15 and x[1]-xPl[i]>0 and war):
                return False
    for i in range(0, len(xComp)-1):
        if(xComp[i]-xComp[i+1] == 0):
            war = y[1]>=min(yComp[i],yComp[i+1]) and y[1]<=max(yComp[i],yComp[i+1])
            if(x[1]-xComp[i]<15 and x[1]-xComp[i]>0 and war):
                return False
    if borders:
        if x[1]<23:
            return False
    if yPl[len(yPl)-1] == y[1] and x[1]-xPl[len(xPl)-1]<12 and x[1]-xPl[len(yPl)-1]>0:
        return False
    if yComp[len(yComp)-1] == y[1] and x[1]-xComp[len(xComp)-1]<12 and x[1]-xComp[len(xComp)-1]>0:
        return False
    if y[0] == y[1] and x[1]-x[0]<12 and x[1]-x[0]>0:
        return False
    for block in blockList:
        if y[1]>block.rect.top and y[1]<block.rect.bottom and x[1]-block.rect.right>0 and x[1]-block.rect.right<10:
            return False
    return True
            
def sprawdz1():
    for i in range(0, len(xPl)-1):
        if(xPl[i]-xPl[i+1] == 0):
            war = y[1]>=min(yPl[i],yPl[i+1]) and y[1]<=max(yPl[i],yPl[i+1])
            if(xPl[i]-x[1]<15 and xPl[i]-x[1]>0 and war):
                return False
    for i in range(0, len(xComp)-1):
        if(xComp[i]-xComp[i+1] == 0):
            war = y[1]>=min(yComp[i],yComp[i+1]) and y[1]<=max(yComp[i],yComp[i+1])
            if(xComp[i]-x[1]<15 and xComp[i]-x[1]>0 and war):
                return False
    if borders:
        if x[1]>size[0]-23:
            return False
    if yPl[len(yPl)-1] == y[1] and xPl[len(xPl)-1]-x[1]>0 and xPl[len(yPl)-1]-x[1]<12:
        return False
    if yComp[len(yComp)-1] == y[1] and xComp[len(xComp)-1]-x[1]<12 and xComp[len(xComp)-1]-x[1]>0:
        return False
    if y[0] == y[1] and x[0]-x[1]<12 and x[0]-x[1]>0:
        return False
    for block in blockList:
        if y[1]>block.rect.top and y[1]<block.rect.bottom and block.rect.left-x[1]>0 and block.rect.left-x[1]<10:
            return False
    return True
    
def best0(a, b, c):
    posDir[0] = sprawdz0()
    posDir[1] = sprawdz1()
    posDir[3] = sprawdz3()
    for block in blockList:
        if y[1]-block.rect.bottom>0 and y[1]-block.rect.bottom<10 and block.rect.x<x[1] and block.rect.right>x[1]:
            if not posDir[1]:
                return 3
            if not posDir[3]:
                return 1
            if x[1]-block.rect.x+abs(xPt-block.rect.x) > block.rect.right-x[1]+abs(xPt-block.rect.right):
                return 1
            else:
                return 3
    if posDir[a]:
        return a
    if posDir[b]:
        return b
    if posDir[c]:
        return c
        
def best1(a, b, c):
    posDir[0] = sprawdz0()
    posDir[1] = sprawdz1()
    posDir[2] = sprawdz2()
    for block in blockList:
        if block.rect.x-x[1]>0 and block.rect.x-x[1]<10 and block.rect.y<y[1] and block.rect.bottom>y[1]:
            if not posDir[0]:
                return 2
            if not posDir[2]:
                return 0
            if y[1]-block.rect.y+abs(yPt-block.rect.y) > block.rect.bottom-y[1]+abs(yPt-block.rect.bottom):
                return 2
            else:
                return 0
    if posDir[a]:
        return a
    if posDir[b]:
        return b
    if posDir[c]:
        return c
                
def best2(a, b, c): #3,2,1
    posDir[1] = sprawdz1()
    posDir[2] = sprawdz2()
    posDir[3] = sprawdz3()
    for block in blockList:
        if block.rect.y-y[1]>0 and block.rect.y-y[1]<10 and block.rect.x<x[1] and block.rect.right>x[1]:
            if not posDir[1]:
                return 3
            if not posDir[3]:
                return 1
            if x[1]-block.rect.x+abs(xPt-block.rect.x) > block.rect.right-x[1]+abs(xPt-block.rect.right):
                return 1
            else:
                return 3
    if posDir[a]:
        return a
    if posDir[b]:
        return b
    if posDir[c]:
        return c
        
def best3(a, b, c):
    posDir[0] = sprawdz0()
    posDir[2] = sprawdz2()
    posDir[3] = sprawdz3()
    for block in blockList:
        if x[1]-block.rect.x>0 and x[1]-block.rect.x<10 and block.rect.y<y[1] and block.rect.bottom>y[1]:
            if not posDir[0]:
                return 2
            if not posDir[2]:
                return 0
            if y[1]-block.rect.y+abs(yPt-block.rect.y) > block.rect.bottom-y[1]+abs(yPt-block.rect.bottom):
                return 2
            else:
                return 0
    if posDir[a]:
        return a
    if posDir[b]:
        return b
    if posDir[c]:
        return c
        
 
# -------- Glowny program -----------
while not done:
    # --- Zdarzenia
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):
                kier[0] = 0
                if accel:
                    v[0] = 2
            elif(event.key == pygame.K_RIGHT):
                kier[0] = 1
                if accel:
                    v[0] = 2
            elif(event.key == pygame.K_DOWN):
                kier[0] = 2
                if accel:
                    v[0] = 2
            elif(event.key == pygame.K_LEFT):
                kier[0] = 3
                if accel:
                    v[0] = 2
            elif(event.key == pygame.K_w):
                kier[1] = 0
                if accel:
                    v[1] = 2
            elif(event.key == pygame.K_d):
                kier[1] = 1
                if accel:
                    v[1] = 2
            elif(event.key == pygame.K_s):
                kier[1] = 2
                if accel:
                    v[1] = 2
            elif(event.key == pygame.K_a):
                kier[1] = 3
                if accel:
                    v[1] = 2
            elif(event.key == pygame.K_ESCAPE):
                if menu:
                    done = True
                else:
                    menu = True
                    gra = False
                    graKomp = False
                    multi = False
                    x = [size[0]//2//SNWIDTH*SNWIDTH+5, 105]
                    y = [size[1]//2//SNWIDTH*SNWIDTH+5, 55]
                    poz = [ [[50, 0]], [[50, 1]] ]
                    kier = [0, 1]
                    v = [1, 1]
                    vx = [0, v[1]]
                    vy = [-v[0], 0]
                    xPl = []
                    yPl = []
                    xPt = -1
                    yPt = -1
                    pointed = True
                    point = None
                    score = [0, 0]
                    prevScore = [0, 0]
                    waz = [ [SnPart()], [SnPart()] ]
                    head = [SnPart(), SnPart()]
                    scrList = [ [], [] ]
                    tmpScrList = [ [], [] ]
                    objectList = pygame.sprite.Group()
                    tmpList = pygame.sprite.Group()
                    objectList.add(waz[0])
                    objectList.add(waz[1])
                    for i in range(0, 2):
                        rysujWeza(x[i], y[i], head[i], waz[i], i, poz[i])
                    for w in waz:
                        for part in w:
                            tmpList.add(part)
                    tmpList.add(head[0])
                    tmpList.add(head[1])
                    tmp = Block(1, 23, random.randrange(0, 61)*10+10, random.randrange(1, 44)*10)
                    while pygame.sprite.spritecollideany(tmp, tmpList) != None or tmp.rect.x<MARG or tmp.rect.y<MARGT or tmp.rect.right>size[0]-MARG or tmp.rect.bottom>size[1]-MARG:
                        tmp = Block(1, 23, random.randrange(0, 61)*10+10, random.randrange(1, 44)*10)
                    tmpBlockList = []
                    tmpBlockList.append(tmp)
                    objectList.add(tmp)
                    tmpList.add(tmp)
                    tmp = Block(37, 1, random.randrange(0, 61)*10+10, random.randrange(1, 44)*10)
                    while pygame.sprite.spritecollideany(tmp, tmpList) != None or tmp.rect.x<MARG or tmp.rect.y<MARGT or tmp.rect.right>size[0]-MARG or tmp.rect.bottom>size[1]-MARG:
                        tmp = Block(37, 1, random.randrange(0, 61)*10+10, random.randrange(1, 44)*10)
                    tmpBlockList.append(tmp)
                    blockList = tmpBlockList
                    objectList.add(tmp)
                    tmpList.add(tmp)
                    lengthen = [0, 0]
                    przegr = [False, False]
                    zablok = [[], []]
                    end = False
            elif(event.key == pygame.K_1):
                menu = False
                gra = True
                graKomp = False
                multi = False
                objectList.remove(waz[1])
            elif(event.key == pygame.K_2):
                menu = False
                gra = False
                graKomp = True
                multi = False
                objectList.add(waz[1])
            elif(event.key == pygame.K_3):
                menu = False
                gra = False
                graKomp = False
                multi = True
                objectList.add(waz[1])
        elif(event.type == pygame.KEYUP):
            if accel:
                if(event.key == pygame.K_UP):
                    kier[0] = 0
                    v[0] = 1
                elif(event.key == pygame.K_RIGHT):
                    kier[0] = 1
                    v[0] = 1
                elif(event.key == pygame.K_DOWN):
                    kier[0] = 2
                    v[0] = 1
                elif(event.key == pygame.K_LEFT):
                    kier[0] = 3
                    v[0] = 1
                elif(event.key == pygame.K_w):
                    kier[1] = 0
                    v[1] = 1
                elif(event.key == pygame.K_d):
                    kier[1] = 1
                    v[1] = 1
                elif(event.key == pygame.K_s):
                    kier[1] = 2
                    v[1] = 1
                elif(event.key == pygame.K_a):
                    kier[1] = 3
                    v[1] = 1
        elif(event.type == pygame.MOUSEMOTION):
            mouse = (event.pos[0], event.pos[1])
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            if(event.button == 1):
                mouseLeft = True
                if mouseClicked == False and abs(mouse[0]-58)<50 and abs(mouse[1]-18)<10:
                    blocks = not blocks
                    mouseClicked = True
                elif mouseClicked == False and abs(mouse[0]-64)<58 and abs(mouse[1]-40)<10:
                    accel = not accel
                    mouseClicked = True
                elif mouseClicked == False and abs(mouse[0]-79)<71 and abs(mouse[1]-62)<10:
                    borders = not borders
                    mouseClicked = True
        elif(event.type == pygame.MOUSEBUTTONUP):
            mouseLeft = False
            mouseClicked = False
        elif(event.type == pygame.QUIT):
            done = True
            
    if blocks:
        blockList = tmpBlockList
        for block in blockList:
            objectList.add(block)
    else:
        blockList = []
        for block in tmpBlockList:
            objectList.remove(block)
    if pointed:
            xPt = ((random.randrange(size[0]-2*MARG-20))//SNWIDTH+2)*SNWIDTH+5
            yPt = ((random.randrange(size[1]-MARG-MARGT-20)+MARGT)//SNWIDTH+1)*SNWIDTH+5
            point = Point(xPt, yPt)
            while pygame.sprite.spritecollideany(point, objectList) != None:
                xPt = ((random.randrange(size[0]-2*MARG-20))//SNWIDTH+2)*SNWIDTH+5
                yPt = ((random.randrange(size[1]-MARG-MARGT-20)+MARGT)//SNWIDTH+1)*SNWIDTH+5
                point = Point(xPt, yPt)
            pointed = False
    if(gra and not end):
        # --- Obliczenia
        zablok[0] = [False]*4
        zablok[0][(poz[0][0][1]+2)%4] = True
        if(poz[0][0][1] == 1 or poz[0][0][1] == 3):
            if(kier[0] == 0): # przy skrecie w gore
                if(x[0]%SNWIDTH == 5):
                    poz[0].insert(0, [SNWIDTH, 0])
                if accel:
                    if(x[0]%SNWIDTH == 6):
                        x[0] -= 1
                        if poz[0][0][1] == 1:
                            poz[0][0][0] -= 1
                            poz[0][len(poz[0])-1][0] += 1
                        else:
                            poz[0][0][0] += 1
                            poz[0][len(poz[0])-1][0] -= 1
                        poz[0].insert(0, [SNWIDTH, 0])
                    elif(x[0]%SNWIDTH == 4):
                        x[0] += 1
                        if poz[0][0][1] == 1:
                            poz[0][0][0] += 1
                            poz[0][len(poz[0])-1][0] -= 1
                        else:
                            poz[0][0][0] -= 1
                            poz[0][len(poz[0])-1][0] += 1
                        poz[0].insert(0, [SNWIDTH, 0])
            elif(kier[0] == 2):
                if(x[0]%SNWIDTH == 5):
                    poz[0].insert(0, [SNWIDTH, 2])
                if accel:
                    if(x[0]%SNWIDTH == 6):
                        x[0] -= 1
                        if poz[0][0][1] == 1:
                            poz[0][0][0] -= 1
                            poz[0][len(poz[0])-1][0] += 1
                        else:
                            poz[0][0][0] += 1
                            poz[0][len(poz[0])-1][0] -= 1
                        poz[0].insert(0, [SNWIDTH, 2])
                    elif(x[0]%SNWIDTH == 4):
                        x[0] += 1
                        if poz[0][0][1] == 1:
                            poz[0][0][0] += 1
                            poz[0][len(poz[0])-1][0] -= 1
                        else:
                            poz[0][0][0] -= 1
                            poz[0][len(poz[0])-1][0] += 1
                        poz[0].insert(0, [SNWIDTH, 2])
        else:
            if(kier[0] == 1): # przy skrecie w prawo
                if(y[0]%SNWIDTH == 5):
                    poz[0].insert(0, [SNWIDTH, 1])
                if accel:
                    if(y[0]%SNWIDTH == 6):
                        y[0] -= 1
                        if poz[0][0][1] == 0:
                            poz[0][0][0] += 1
                            poz[0][len(poz[0])-1][0] -= 1
                        else:
                            poz[0][0][0] -= 1
                            poz[0][len(poz[0])-1][0] += 1
                        poz[0].insert(0, [SNWIDTH, 1])
                    elif(y[0]%SNWIDTH == 4):
                        y[0] += 1
                        if poz[0][0][1] == 0:
                            poz[0][0][0] -= 1
                            poz[0][len(poz[0])-1][0] += 1
                        else:
                            poz[0][0][0] += 1
                            poz[0][len(poz[0])-1][0] -= 1
                        poz[0].insert(0, [SNWIDTH, 1])
            elif(kier[0] == 3):
                if(y[0]%SNWIDTH == 5):
                    poz[0].insert(0, [SNWIDTH, 3])
                if accel:
                    if(y[0]%SNWIDTH == 6):
                        y[0] -= 1
                        if poz[0][0][1] == 0:
                            poz[0][0][0] += 1
                            poz[0][len(poz[0])-1][0] -= 1
                        else:
                            poz[0][0][0] -= 1
                            poz[0][len(poz[0])-1][0] += 1
                        poz[0].insert(0, [SNWIDTH, 3])
                    elif(y[0]%SNWIDTH == 4):
                        y[0] += 1
                        if poz[0][0][1] == 0:
                            poz[0][0][0] -= 1
                            poz[0][len(poz[0])-1][0] += 1
                        else:
                            poz[0][0][0] += 1
                            poz[0][len(poz[0])-1][0] -= 1
                        poz[0].insert(0, [SNWIDTH, 3])
        
        if(poz[0][0][1] == 0 and (not zablok[0][0])):
            vx[0] = 0
            vy[0] = -v[0]
        elif(poz[0][0][1] == 1 and (not zablok[0][1])):
            vx[0] = v[0]
            vy[0] = 0
        elif(poz[0][0][1] == 2 and (not zablok[0][2])):
            vx[0] = 0
            vy[0] = v[0]
        elif(poz[0][0][1] == 3 and (not zablok[0][3])):
            vy[0] = 0
            vx[0] = -v[0]
        poz[0][0][0] += v[0]
        poz[0][len(poz[0])-1][0] -= v[0]
        x[0] += vx[0]
        x[0] %= size[0]
        y[0] += vy[0]
        y[0] %= size[1]
        if(poz[0][len(poz[0])-1][0] <= SNWIDTH):
            del poz[0][len(poz[0])-1]
        if(lengthen[0] > 0):
            poz[0][len(poz[0])-1][0] += 1
            lengthen[0] -= 1
        if(x[0] == xPt and abs(y[0]-yPt)<SNWIDTH):
            pointed = True
            score[0] += 1
            poz[0][len(poz[0])-1][0] += 1
            lengthen[0] += 19
        if(y[0] == yPt and abs(x[0]-xPt)<SNWIDTH):
            pointed = True
            score[0] += 1
            poz[0][len(poz[0])-1][0] += 1
            lengthen[0] += 19
        # --- Rysowanie
        for i in range(0, len(poz[0])-len(waz[0])):
            waz[0].append(SnPart())
            objectList.add(waz[0][len(waz[0])-1])
        for i in range(0, len(waz[0])-len(poz[0])):
            o = len(waz[0])-1
            objectList.remove(waz[0][o])
            del waz[0][o]
        # Czyszczenie ekranu
        screen.fill(BLACK)
        if borders:
            pygame.draw.rect(screen, WHITE, (MARG, MARGT, width, height+MARG-MARGT), 2)
        scrList[0] = rysujWeza(x[0], y[0], head[0], waz[0], 0, poz[0])
        for scr in tmpScrList[0]:
            objectList.remove(scr)
        tmpScrList[0] = []
        for scr in scrList[0]:
            objectList.add(scr)
            tmpScrList[0].append(scr)
        if pygame.sprite.spritecollideany(head[0], objectList) != None:
            end = True
            text = font.render("Przegraleś", True, WHITE, BLACK)
            xText = (size[0]-text.get_width())//2
            screen.blit(text, (xText, 8))
        if borders:
            if(x[0]<12 or y[0]<37 or x[0]>size[0]-11 or y[0]>size[1]-11):
                end = True
                text = font.render("Przegraleś", True, WHITE, BLACK)
                xText = (size[0]-text.get_width())//2
                screen.blit(text, (xText, 8))
        # --- Rysowanie na ekran
        scoreText = font.render("Wynik: "+str(score[0]), True, WHITE, BLACK)
        screen.blit(scoreText, (8, 8))
        screen.blit(head[0].image, (head[0].rect.x, head[0].rect.y))
        screen.blit(point.image, (point.rect.x, point.rect.y))
        objectList.draw(screen)
    elif graKomp and not end:
        if accel:
            v[1] = 2
        xPl = [x[0]]
        yPl = [y[0]]
        xComp = [x[1]]
        yComp = [y[1]]
        for i in range(0, len(poz[0])):
            if(poz[0][i][1] == 0):
                xPl.append(xPl[i])
                yPl.append((yPl[i]+poz[0][i][0]-SNWIDTH)% size[1])
            elif(poz[0][i][1] == 1):
                xPl.append((xPl[i]-poz[0][i][0]+SNWIDTH)%size[0])
                yPl.append(yPl[i])
            elif(poz[0][i][1] == 2):
                xPl.append(xPl[i])
                yPl.append((yPl[i]-poz[0][i][0]+SNWIDTH)%size[1])
            else:
                xPl.append((xPl[i]+poz[0][i][0]-SNWIDTH)%size[0])
                yPl.append(yPl[i])
        for i in range(0, len(poz[1])):
            if(poz[1][i][1] == 0):
                xComp.append(xComp[i])
                yComp.append((yComp[i]+poz[1][i][0]-SNWIDTH)%size[1])
            elif(poz[1][i][1] == 1):
                xComp.append((xComp[i]-poz[1][i][0]+SNWIDTH)%size[0])
                yComp.append(yComp[i])
            elif(poz[1][i][1] == 2):
                xComp.append(xComp[i])
                yComp.append((yComp[i]-poz[1][i][0]+SNWIDTH)%size[1])
            else:
                xComp.append((xComp[i]+poz[1][i][0]-SNWIDTH)%size[0])
                yComp.append(yComp[i])
        if borders:
            if(x[1] < xPt):
                if(y[1] > yPt):
                    if(poz[1][0][1] == 0):
                        kier[1] = best0(0,1,3)
                    elif(poz[1][0][1] == 1):
                        kier[1] = best1(1,0,2)
                    elif(poz[1][0][1] == 2):
                        kier[1] = best2(1,2,3)
                    else:
                        kier[1] = best3(0,3,2)
                elif(y[1] < yPt):
                    if(poz[1][0][1] == 0):
                        kier[1] = best0(1,0,3)
                    elif(poz[1][0][1] == 1):
                        kier[1] = best1(1,2,0)
                    elif(poz[1][0][1] == 2):
                        kier[1] = best2(2,1,3)
                    else:
                        kier[1] = best3(2,3,0)
                else:
                    if(poz[1][0][1] == 0):
                        kier[1] = best0(1,0,3)
                    elif(poz[1][0][1] == 1):
                        kier[1] = best1(1,2,0)
                    elif(poz[1][0][1] == 2):
                        kier[1] = best2(1,2,3)
                    else:
                        kier[1] = best3(0,2,3)
            elif(x[1] > xPt):
                if(y[1] > yPt):
                    if(poz[1][0][1] == 0):
                        kier[1] = best0(0,3,1)
                    elif(poz[1][0][1] == 1):
                        kier[1] = best1(0,1,2)
                    elif(poz[1][0][1] == 2):
                        kier[1] = best2(3,2,1)
                    else:
                        kier[1] = best3(3,0,2)
                elif(y[1] < yPt):
                    if(poz[1][0][1] == 0):
                        kier[1] = best0(3,0,1)
                    elif(poz[1][0][1] == 1):
                        kier[1] = best1(2,1,0)
                    elif(poz[1][0][1] == 2):
                        kier[1] = best2(2,3,1)
                    else:
                        kier[1] = best3(3,2,0)
                else:
                    if(poz[1][0][1] == 0):
                        kier[1] = best0(3,1,0)
                    elif(poz[1][0][1] == 1):
                        kier[1] = best1(0,2,1)
                    elif(poz[1][0][1] == 2):
                        kier[1] = best2(3,2,1)
                    else:
                        kier[1] = best3(3,0,2)
            else:
                if(y[1] > yPt):
                    if(poz[1][0][1] == 0):
                        kier[1] = best0(0,1,3)
                    elif(poz[1][0][1] == 1):
                        kier[1] = best1(0,1,2)
                    elif(poz[1][0][1] == 2):
                        kier[1] = best2(1,3,2)
                    else:
                        kier[1] = best3(0,3,2)
                else:
                    if(poz[1][0][1] == 0):
                        kier[1] = best0(1,3,0)
                    elif(poz[1][0][1] == 1):
                        kier[1] = best1(2,1,0)
                    elif(poz[1][0][1] == 2):
                        kier[1] = best2(2,1,3)
                    else:
                        kier[1] = best3(2,3,0)
        else:
            if x[1] == xPt:
                if (y[1]-yPt)%size[1] < size[1]//2: # w gore krocej
                    if poz[1][0][1] == 0:
                        kier[1] = best0(0,3,1)
                    if poz[1][0][1] == 1:
                        kier[1] = best1(0,1,2)
                    if poz[1][0][1] == 2:
                        kier[1] = best2(2,3,1)
                    if poz[1][0][1] == 3:
                        kier[1] = best3(0,3,2)
                else:
                    if poz[1][0][1] == 0:
                        kier[1] = best0(0,1,3)
                    if poz[1][0][1] == 1:
                        kier[1] = best1(2,1,0)
                    if poz[1][0][1] == 2:
                        kier[1] = best2(2,3,1)
                    if poz[1][0][1] == 3:
                        kier[1] = best3(2,3,0)
            elif (x[1]-xPt)%size[0] < size[0]//2: # w lewo krocej
                if y[1] == yPt:
                    if poz[1][0][1] == 0:
                        kier[1] = best0(3,1,0)
                    if poz[1][0][1] == 1:
                        kier[1] = best1(1,0,2)
                    if poz[1][0][1] == 2:
                        kier[1] = best2(3,1,2)
                    if poz[1][0][1] == 3:
                        kier[1] = best3(3,0,2)
                elif (y[1]-yPt)%size[1] < size[1]//2: # w gore krocej
                    if poz[1][0][1] == 0:
                        kier[1] = best0(0,3,1)
                    if poz[1][0][1] == 1:
                        kier[1] = best1(1,0,2)
                    if poz[1][0][1] == 2:
                        kier[1] = best2(3,2,1)
                    if poz[1][0][1] == 3:
                        kier[1] = best3(3,0,2)
                else:
                    if poz[1][0][1] == 0:
                        kier[1] = best0(3,0,1)
                    if poz[1][0][1] == 1:
                        kier[1] = best1(1,2,0)
                    if poz[1][0][1] == 2:
                        kier[1] = best2(2,3,1)
                    if poz[1][0][1] == 3:
                        kier[1] = best3(3,2,0)
            else: # w prawo krocej
                if y[1] == yPt:
                    if poz[1][0][1] == 0:
                        kier[1] = best0(1,3,0)
                    if poz[1][0][1] == 1:
                        kier[1] = best1(1,0,2)
                    if poz[1][0][1] == 2:
                        kier[1] = best2(1,3,2)
                    if poz[1][0][1] == 3:
                        kier[1] = best3(3,0,2)
                elif (y[1]-yPt)%size[1] < size[1]//2: # w gore krocej
                    if poz[1][0][1] == 0:
                        kier[1] = best0(0,1,3)
                    if poz[1][0][1] == 1:
                        kier[1] = best1(1,0,2)
                    if poz[1][0][1] == 2:
                        kier[1] = best2(1,2,3)
                    if poz[1][0][1] == 3:
                        kier[1] = best3(0,3,2)
                else:
                    if poz[1][0][1] == 0:
                        kier[1] = best0(1,0,3)
                    if poz[1][0][1] == 1:
                        kier[1] = best1(1,2,0)
                    if poz[1][0][1] == 2:
                        kier[1] = best2(1,2,3)
                    if poz[1][0][1] == 3:
                        kier[1] = best3(2,3,0)
        # Obliczenia
        for i in range(0,2):
            zablok[i] = [False]*4
            zablok[i][(poz[i][0][1]+2)%4] = True
            if(poz[i][0][1] == 1 or poz[i][0][1] == 3):
                if(kier[i] == 0): # przy skrecie w gore
                    if(x[i]%SNWIDTH == 5):
                        poz[i].insert(0, [SNWIDTH, 0])
                    if accel:
                        if(x[i]%SNWIDTH == 6):
                            x[i] -= 1
                            if poz[i][0][1] == 1:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            else:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            poz[i].insert(0, [SNWIDTH, 0])
                        elif(x[i]%SNWIDTH == 4):
                            x[i] += 1
                            if poz[i][0][1] == 1:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            else:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            poz[i].insert(0, [SNWIDTH, 0])
                elif(kier[i] == 2):
                    if(x[i]%SNWIDTH == 5):
                        poz[i].insert(0, [SNWIDTH, 2])
                    if accel:
                        if(x[i]%SNWIDTH == 6):
                            x[i] -= 1
                            if poz[i][0][1] == 1:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            else:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            poz[i].insert(0, [SNWIDTH, 2])
                        elif(x[i]%SNWIDTH == 4):
                            x[i] += 1
                            if poz[i][0][1] == 1:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            else:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            poz[i].insert(0, [SNWIDTH, 2])
            else:
                if(kier[i] == 1): # przy skrecie w prawo
                    if(y[i]%SNWIDTH == 5):
                        poz[i].insert(0, [SNWIDTH, 1])
                    if accel:
                        if(y[i]%SNWIDTH == 6):
                            y[i] -= 1
                            if poz[i][0][1] == 0:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            else:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            poz[i].insert(0, [SNWIDTH, 1])
                        elif(y[i]%SNWIDTH == 4):
                            y[i] += 1
                            if poz[i][0][1] == 0:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            else:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            poz[i].insert(0, [SNWIDTH, 1])
                elif(kier[i] == 3):
                    if(y[i]%SNWIDTH == 5):
                        poz[i].insert(0, [SNWIDTH, 3])
                    if accel:
                        if(y[i]%SNWIDTH == 6):
                            y[i] -= 1
                            if poz[i][0][1] == 0:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            else:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            poz[i].insert(0, [SNWIDTH, 3])
                        elif(y[i]%SNWIDTH == 4):
                            y[i] += 1
                            if poz[i][0][1] == 0:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            else:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            poz[i].insert(0, [SNWIDTH, 3])
            
            if(poz[i][0][1] == 0 and (not zablok[i][0])):
                vx[i] = 0
                vy[i] = -v[i]
            elif(poz[i][0][1] == 1 and (not zablok[i][1])):
                vx[i] = v[i]
                vy[i] = 0
            elif(poz[i][0][1] == 2 and (not zablok[i][2])):
                vx[i] = 0
                vy[i] = v[i]
            elif(poz[i][0][1] == 3 and (not zablok[i][3])):
                vy[i] = 0
                vx[i] = -v[i]
            poz[i][0][0] += v[i]
            poz[i][len(poz[i])-1][0] -= v[i]
            x[i] += vx[i]
            x[i] %= size[0]
            y[i] += vy[i]
            y[i] %= size[1]
            if(poz[i][len(poz[i])-1][0] <= SNWIDTH):
                del poz[i][len(poz[i])-1]
            if(lengthen[i] > 0):
                poz[i][len(poz[i])-1][0] += 1
                lengthen[i] -= 1
            if(x[i] == xPt and abs(y[i]-yPt)<SNWIDTH):
                pointed = True
                score[i] += 1
                poz[i][len(poz[i])-1][0] += 1
                lengthen[i] += 19
            if(y[i] == yPt and abs(x[i]-xPt)<SNWIDTH):
                pointed = True
                score[i] += 1
                poz[i][len(poz[i])-1][0] += 1
                lengthen[i] += 19
            # uzupelnianie weża
            for j in range(0, len(poz[i])-len(waz[i])):
                last = SnPart()
                waz[i].append(last)
                objectList.add(last)
            for j in range(0, len(waz[i])-len(poz[i])):
                lIndex = len(waz[i])-1
                objectList.remove(waz[i][lIndex])
                del waz[i][lIndex]
        screen.fill(BLACK)
        if borders:
            pygame.draw.rect(screen, WHITE, (MARG, MARGT, width, height+MARG-MARGT), 2)
        for i in range(0, 2):
            for scr in tmpScrList[i]:
                objectList.remove(scr)
            scrList[i] = rysujWeza(x[i], y[i], head[i], waz[i], i, poz[i])
            for scr in scrList[i]:
                objectList.add(scr)
            tmpScrList[i] = []
            for scr in scrList[i]:
                tmpScrList[i].append(scr)
        for i in range(0, 2):
            if pygame.sprite.spritecollideany(head[i], objectList) != None:
                przegr[i] = True
                prevScore[i] = score[i]
                score[i] -= 2
                end = True
            if borders:
                if(x[i]<12 or y[i]<37 or x[i]>size[0]-11 or y[i]>size[1]-11):
                    przegr[i] = True
                    prevScore[i] = score[i]
                    score[i] -= 1
                    end = True
        # rysowanie na ekran
        score0 = font.render("Gracz: {}".format(score[0]), True, WHITE, BLACK)
        screen.blit(score0, (8, 8))
        if prevScore[0] != 0:
            prevScoreText = font14.render(str(score[0]-prevScore[0]), True, WHITE, BLACK)
            screen.blit(prevScoreText, (10+score0.get_width(), 8))
            score1 = font.render("Komputer: {}".format(score[1]), True, WHITE, BLACK)
            screen.blit(score1, (size[0]-score1.get_width()-8, 8))
        elif prevScore[1] != 0:
            prevScoreText = font14.render(str(score[1]-prevScore[1]), True, WHITE, BLACK)
            screen.blit(prevScoreText, (size[0]-prevScoreText.get_width()-8, 8))
            score1 = font.render("Komputer: {}".format(score[1]), True, WHITE, BLACK)
            screen.blit(score1, (size[0]-prevScoreText.get_width()-score1.get_width()-10, 8))
        else:
            score1 = font.render("Komputer: {}".format(score[1]), True, WHITE, BLACK)
            screen.blit(score1, (size[0]-score1.get_width()-8, 8))
        for i in range(0, 2):
            screen.blit(head[i].image, (head[i].rect.x, head[i].rect.y))
        screen.blit(point.image, (point.rect.x, point.rect.y))
        if end:
            if score[1]>score[0]:
                wonText = font.render("Komputer wygrał", True, WHITE, BLACK)
                xText = (size[0]-wonText.get_width())//2
                screen.blit(wonText, (xText, 8))
            elif score[0]>score[1]:
                wonText = font.render("Gracz wygrał", True, WHITE, BLACK)
                xText = (size[0]-wonText.get_width())//2
                screen.blit(wonText, (xText, 8))
            else:
                wonText = font.render("Remis", True, WHITE, BLACK)
                xText = (size[0]-wonText.get_width())//2
                screen.blit(wonText, (xText, 8))
        objectList.draw(screen)
    elif multi and not end:
        # Obliczenia
        for i in range(0,2):
            zablok[i] = [False]*4
            zablok[i][(poz[i][0][1]+2)%4] = True
            if(poz[i][0][1] == 1 or poz[i][0][1] == 3):
                if(kier[i] == 0): # przy skrecie w gore
                    if(x[i]%SNWIDTH == 5):
                        poz[i].insert(0, [SNWIDTH, 0])
                    if accel:
                        if(x[i]%SNWIDTH == 6):
                            x[i] -= 1
                            if poz[i][0][1] == 1:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            else:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            poz[i].insert(0, [SNWIDTH, 0])
                        elif(x[i]%SNWIDTH == 4):
                            x[i] += 1
                            if poz[i][0][1] == 1:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            else:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            poz[i].insert(0, [SNWIDTH, 0])
                elif(kier[i] == 2):
                    if(x[i]%SNWIDTH == 5):
                        poz[i].insert(0, [SNWIDTH, 2])
                    if accel:
                        if(x[i]%SNWIDTH == 6):
                            x[i] -= 1
                            if poz[i][0][1] == 1:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            else:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            poz[i].insert(0, [SNWIDTH, 2])
                        elif(x[i]%SNWIDTH == 4):
                            x[i] += 1
                            if poz[i][0][1] == 1:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            else:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            poz[i].insert(0, [SNWIDTH, 2])
            else:
                if(kier[i] == 1): # przy skrecie w prawo
                    if(y[i]%SNWIDTH == 5):
                        poz[i].insert(0, [SNWIDTH, 1])
                    if accel:
                        if(y[i]%SNWIDTH == 6):
                            y[i] -= 1
                            if poz[i][0][1] == 0:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            else:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            poz[i].insert(0, [SNWIDTH, 1])
                        elif(y[i]%SNWIDTH == 4):
                            y[i] += 1
                            if poz[i][0][1] == 0:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            else:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            poz[i].insert(0, [SNWIDTH, 1])
                elif(kier[i] == 3):
                    if(y[i]%SNWIDTH == 5):
                        poz[i].insert(0, [SNWIDTH, 3])
                    if accel:
                        if(y[i]%SNWIDTH == 6):
                            y[i] -= 1
                            if poz[i][0][1] == 0:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            else:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            poz[i].insert(0, [SNWIDTH, 3])
                        elif(y[i]%SNWIDTH == 4):
                            y[i] += 1
                            if poz[i][0][1] == 0:
                                poz[i][0][0] -= 1
                                poz[i][len(poz[i])-1][0] += 1
                            else:
                                poz[i][0][0] += 1
                                poz[i][len(poz[i])-1][0] -= 1
                            poz[i].insert(0, [SNWIDTH, 3])
            
            if(poz[i][0][1] == 0 and (not zablok[i][0])):
                vx[i] = 0
                vy[i] = -v[i]
            elif(poz[i][0][1] == 1 and (not zablok[i][1])):
                vx[i] = v[i]
                vy[i] = 0
            elif(poz[i][0][1] == 2 and (not zablok[i][2])):
                vx[i] = 0
                vy[i] = v[i]
            elif(poz[i][0][1] == 3 and (not zablok[i][3])):
                vy[i] = 0
                vx[i] = -v[i]
            poz[i][0][0] += v[i]
            poz[i][len(poz[i])-1][0] -= v[i]
            x[i] += vx[i]
            x[i] %= size[0]
            y[i] += vy[i]
            y[i] %= size[1]
            if(poz[i][len(poz[i])-1][0] <= SNWIDTH):
                del poz[i][len(poz[i])-1]
            if(lengthen[i] > 0):
                poz[i][len(poz[i])-1][0] += 1
                lengthen[i] -= 1
            if(x[i] == xPt and abs(y[i]-yPt)<SNWIDTH):
                pointed = True
                score[i] += 1
                poz[i][len(poz[i])-1][0] += 1
                lengthen[i] += 19
            if(y[i] == yPt and abs(x[i]-xPt)<SNWIDTH):
                pointed = True
                score[i] += 1
                poz[i][len(poz[i])-1][0] += 1
                lengthen[i] += 19
            # uzupelnianie weża
            for j in range(0, len(poz[i])-len(waz[i])):
                last = SnPart()
                waz[i].append(last)
                objectList.add(last)
            for j in range(0, len(waz[i])-len(poz[i])):
                lIndex = len(waz[i])-1
                objectList.remove(waz[i][lIndex])
                del waz[i][lIndex]
        screen.fill(BLACK)
        if borders:
            pygame.draw.rect(screen, WHITE, (MARG, MARGT, width, height+MARG-MARGT), 2)
        for i in range(0, 2):
            for scr in tmpScrList[i]:
                objectList.remove(scr)
            scrList[i] = rysujWeza(x[i], y[i], head[i], waz[i], i, poz[i])
            for scr in scrList[i]:
                objectList.add(scr)
            tmpScrList[i] = []
            for scr in scrList[i]:
                tmpScrList[i].append(scr)
        for i in range(0, 2):
            if pygame.sprite.spritecollideany(head[i], objectList) != None:
                przegr[i] = True
                score[i] -= 2
                end = True
            if borders:
                if(x[i]<12 or y[i]<37 or x[i]>size[0]-11 or y[i]>size[1]-11):
                    przegr[i] = True
                    score[i] -= 1
                    end = True
        # rysowanie na ekran
        score0 = font.render("Gracz1: {}".format(score[0]), True, WHITE, BLACK)
        screen.blit(score0, (8, 8))
        if prevScore[0] != 0:
            prevScoreText = font14.render(str(score[0]-prevScore[0]), True, WHITE, BLACK)
            screen.blit(prevScoreText, (10+score0.get_width(), 8))
            score1 = font.render("Gracz2: {}".format(score[1]), True, WHITE, BLACK)
            screen.blit(score1, (size[0]-score1.get_width()-8, 8))
        elif prevScore[1] != 0:
            prevScoreText = font14.render(str(score[1]-prevScore[1]), True, WHITE, BLACK)
            screen.blit(prevScoreText, (size[0]-prevScoreText.get_width()-8, 8))
            score1 = font.render("Gracz2: {}".format(score[1]), True, WHITE, BLACK)
            screen.blit(score1, (size[0]-prevScoreText.get_width()-score1.get_width()-10, 8))
        else:
            score1 = font.render("Gracz2: {}".format(score[1]), True, WHITE, BLACK)
            screen.blit(score1, (size[0]-score1.get_width()-8, 8))
        for i in range(0, 2):
            screen.blit(head[i].image, (head[i].rect.x, head[i].rect.y))
        screen.blit(point.image, (point.rect.x, point.rect.y))
        if end:
            if score[1]>score[0]:
                wonText = font.render("Gracz2 wygral", True, WHITE, BLACK)
                xText = (size[0]-wonText.get_width())//2
                screen.blit(wonText, (xText, 8))
            elif score[0]>score[1]:
                wonText = font.render("Gracz1 wygral", True, WHITE, BLACK)
                xText = (size[0]-wonText.get_width())//2
                screen.blit(wonText, (xText, 8))
            else:
                wonText = font.render("Remis", True, WHITE, BLACK)
                xText = (size[0]-wonText.get_width())//2
                screen.blit(wonText, (xText, 8))
        objectList.draw(screen)
    elif menu: # menu
        screen.fill(BLACK)
        if blocks:
            screen.blit(przeszkodyActive, (8, 8))
        else:
            screen.blit(przeszkodyInactive, (8, 8))
        if accel:
            screen.blit(aActive, (8, 30))
        else:
            screen.blit(aInactive, (8, 30))
        if borders:
            screen.blit(krActive, (8, 52))
        else:
            screen.blit(krInactive, (8, 52))
        if abs(mouse[0]-size[0]//2)<91 and abs(mouse[1]-122)<22:
            screen.blit(grajActive, ((size[0]-183)//2, 100))
            screen.blit(kompInactive, ((size[0]-183)//2, 150))
            screen.blit(multiInactive, ((size[0]-183)//2, 200))
            if mouseLeft:
                menu = False
                gra = True
                objectList.remove(waz[1])
        elif abs(mouse[0]-size[0]//2)<91 and abs(mouse[1]-172)<22:
            screen.blit(grajInactive, ((size[0]-183)//2, 100))
            screen.blit(kompActive, ((size[0]-183)//2, 150))
            screen.blit(multiInactive, ((size[0]-183)//2, 200))
            if mouseLeft:
                menu = False
                graKomp = True
                objectList.add(waz[1])
        elif abs(mouse[0]-size[0]//2)<91 and abs(mouse[1]-222)<22:
            screen.blit(grajInactive, ((size[0]-183)//2, 100))
            screen.blit(kompInactive, ((size[0]-183)//2, 150))
            screen.blit(multiActive, ((size[0]-183)//2, 200))
            if mouseLeft:
                menu = False
                multi = True
                objectList.add(waz[1])
        else:
            screen.blit(grajInactive, ((size[0]-183)//2, 100))
            screen.blit(kompInactive, ((size[0]-183)//2, 150))
            screen.blit(multiInactive, ((size[0]-183)//2, 200))
    pygame.display.flip()
 
    # --- 60 klatek na sekunde
    clock.tick(60)
pygame.quit() # zamknij wszystkie okna
