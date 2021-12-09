import sys, time
import pygame
from pygame.locals import *
#from pygame.locals import *

xWinSize = 1100
yWinSize = 650

#xWinSize = int(input("x:"))
#yWinSize = int(input("y:"))

current = 0

maps = []
mapWidths = []
mapHeights = []

file = open("map1.txt", "r")
mapWidths.append(int(file.readline()))
mapHeights.append(int(file.readline()))
maps.append(list(file.readline()))
file.close()


file = open("map2.txt", "r")
mapWidths.append(int(file.readline()))
mapHeights.append(int(file.readline()))
maps.append(list(file.readline()))
file.close()

file = open("map3.txt", "r")
mapWidths.append(int(file.readline()))
mapHeights.append(int(file.readline()))
maps.append(list(file.readline()))
file.close()

file = open("map4.txt", "r")
mapWidths.append(int(file.readline()))
mapHeights.append(int(file.readline()))
maps.append(list(file.readline()))
file.close()

file = open("map5.txt", "r")
mapWidths.append(int(file.readline()))
mapHeights.append(int(file.readline()))
maps.append(list(file.readline()))
file.close()

bMap = maps[current][:]



fps = 1/60
tileSize = 32*2
xMapSize = mapWidths[current]*tileSize
yMapSize = mapHeights[current]*tileSize
xVisibleTiles = xWinSize/tileSize+5
yVisibleTiles = yWinSize/tileSize+5
xOffset = 0
yOffset = 0
#gradual offset
xGset = 0
yGset = 0
onGround = False
jump = False
dead = False
vic = False
coin = False



def m2p(x, y):
    if x >= 0 and x < mapWidths[current] and y >= 0 and y < mapHeights[current]:
        return x*tileSize, y*tileSize
    else:
        return 0


xNew, yNew = m2p(1,0)
p1x = 0
p1y = 0
camx = p1x
camy = p1y
velx = 0
vely = 0
s = 6
j = 25
v = j
g = 6
coins = 0



def getTile(x, y):
    if x >= 0 and x < mapWidths[current] and y >= 0 and y < mapHeights[current]:
        return maps[current][y * mapWidths[current] + x]
    else:
        return '0'

def setTile(x, y, i):
    if x >= 0 and x < mapWidths[current] and y >= 0 and y < mapHeights[current]:
        maps[current][y * mapWidths[current] + x] = i

def getTile2(x,y):
    if x >= 0 and x < xMapSize and y >= 0 and y < yMapSize:
        return maps[current][int(y/tileSize)*mapWidths[current]+int(x/tileSize)]
    else:
        return 0



def drawMap():
    global xVisibleTiles, yVisibleTiles, xOffset, yOffset, xMapSize, yMapSize, camx, camy, xGset, yGset, current

    xOffset = camx+(tileSize/2) - xWinSize/2
    yOffset = camy+(tileSize/2) - yWinSize/2

    if xOffset < 0:
        xOffset = 0
    if yOffset < 0:
        yOffset = 0

    if xOffset > xMapSize-xWinSize:
        xOffset = xMapSize - xWinSize

    
    if yOffset > yMapSize-yWinSize:
        yOffset = yMapSize - yWinSize


    xGset = xOffset % tileSize
    yGset = yOffset % tileSize
    
    
    
    x = 0
    y = 0
    while y < yVisibleTiles:
        while x < xVisibleTiles:
            ID = getTile(x+int(xOffset/tileSize), y+int(yOffset/tileSize))

            bx = x*tileSize - xGset
            by = y*tileSize - yGset
            
            if ID == '1':
                    win.blit(blockTexes[current%2], (bx, by), (0,0,tileSize,tileSize))
            elif ID == '2':
                    win.blit(blockTexes[current%2], (bx, by), (tileSize,0,tileSize,tileSize))
            elif ID == '3':
                    win.blit(blockTexes[current%2], (bx, by), (tileSize,tileSize,tileSize,tileSize))
            x+=1
        y+=1
        x=0
    y=0

def handleEvents():
    global velx, vely, s, onGround, jump, dead, pos, coin, coins
    
    vely = 1

    for event in pygame.event.get():
        
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                velx = 1
            elif event.key == pygame.K_a:
                velx = -1
            elif event.key == pygame.K_w:
                if onGround:
                    jump = True
            elif event.key == pygame.K_s:
                vely = 4
            elif event.key == pygame.K_r:
                dead = True
            elif event.key == pygame.K_c:
                x,y = pygame.mouse.get_pos()
                setTile(int((x+xOffset)/tileSize),int((y+yOffset)/tileSize), '1')
            elif event.key == pygame.K_x:
                x,y = pygame.mouse.get_pos()
                setTile(int((x+xOffset)/tileSize),int((y+yOffset)/tileSize), '0')
            elif event.key == pygame.K_l:
                coin = True
                coins+=1


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                if velx > 0:
                    velx = 0
            elif event.key == pygame.K_a:
                if velx < 0:
                    velx = 0

def drawPlayer():
    global xOffset, yOffset, p1x, p1y, velx, vely, current
    p1x = xNew
    p1y = yNew
    win.blit(blockTexes[current%2], (p1x-xOffset, p1y-yOffset), (0, tileSize, tileSize, tileSize))
    pygame.draw.rect(win, (255,255,255), (0,0,90,64))
    win.blit(scoreTex, (0,0))
    #velx = 0
    #vely = 0

def collision():
    global velx, vely, p1x, p1y, tileSize, xNew, yNew, onGround, dead, jump, vic, coin, coins, v, j
    #left right
    if velx != 0:
        #right
        if velx > 0:
            topRight = getTile(int(xNew/tileSize+0.99), int(p1y/tileSize))
            bottomRight = getTile(int(xNew/tileSize+0.99), int(p1y/tileSize+0.99))
            
            if topRight == '1' or bottomRight == '1':
                xNew = int(xNew/tileSize)*tileSize

            elif topRight == '2' or bottomRight == '2':
                dead = True

            elif topRight == '3':
                setTile(int(xNew/tileSize+0.99), int(p1y/tileSize), '0')
                coin=True
                coins+=1
            elif bottomRight == '3':
                setTile(int(xNew/tileSize+0.99), int(p1y/tileSize+0.99), '0')
                coin=True
                coins+=1

        #left
        elif velx < 0:
            topLeft = getTile(int(xNew/tileSize), int(p1y/tileSize))
            bottomLeft = getTile(int(xNew/tileSize), int(p1y/tileSize+0.99))

            if topLeft == '1' or bottomLeft == '1':
                xNew = int(xNew/tileSize+1)*tileSize

            elif topLeft == '2' or bottomLeft == '2':
                dead = True

            elif topLeft == '3':
                setTile(int(xNew/tileSize), int(p1y/tileSize), '0')
                coin=True
                coins+=1
            elif bottomLeft == '3':
                setTile(int(xNew/tileSize), int(p1y/tileSize+0.99), '0')
                coin=True
                coins+=1
                
    #up down
    if vely != 0:
        #down
        if vely > 0:
            bottomLeft = getTile(int(xNew/tileSize), int(yNew/tileSize+0.99))
            bottomRight = getTile(int(xNew/tileSize+0.99), int(yNew/tileSize+0.99))
            
            if bottomLeft == '1' or bottomRight == '1':
                yNew = int(yNew/tileSize)*tileSize
                onGround = True

            elif bottomLeft == '2' or bottomRight == '2':
                dead = True

            elif bottomLeft == '3':
                setTile(int(xNew/tileSize), int(yNew/tileSize+0.99), '0')
                coin=True
                coins+=1
            elif bottomRight == '3':
                setTile(int(xNew/tileSize+0.99), int(yNew/tileSize+0.99), '0')
                coin=True
                coins+=1
            
        #up
        elif vely < 0:
            topLeft = getTile(int(xNew/tileSize), int(yNew/tileSize))
            topRight = getTile(int(xNew/tileSize+0.99), int(yNew/tileSize))
            
            if topLeft == '1' or topRight == '1':
                yNew = int(yNew/tileSize+1)*tileSize
                jump = False
                v = j

            elif topLeft == '2' or topRight == '2':
                dead = True
                jump = False

            elif topLeft == '3':
                setTile(int(xNew/tileSize), int(yNew/tileSize), '0')
                coin=True
                coins+=1
            elif topRight == '3':
                setTile(int(xNew/tileSize+0.99), int(yNew/tileSize), '0')
                coin=True
                coins+=1



                
def update():
    global xNew, yNew, velx, vely, camx, camy, p1x, p1y, onGround, jump, v, dead, vic, map1, bMap, coins, coin, scoreTex, mFont, j, current, win, xMapSize
    global yMapSize, mapWidths, mapHeights
    xNew += velx*s
    #gravity
    if jump:
        vely = -1
        
        yNew += vely*v
        v-=(g/4)
        if v < 0:
            jump = False
            v = j
    else:
        yNew += vely*g

    if dead:
        dead = False
        xNew, yNew = m2p(1, 0)
        coins=0
        v = j
        scoreTex = mFont.render(str(coins), False, (0, 0, 0))
        maps[current] = bMap[:]
    elif coin:
        if coins >= 7:
            print("Win!")
            scoreTex = mFont.render("Win", False, (0, 0, 0))
            if current < len(maps)-1:
                current+=1

            print(current)
            coins = 0
            scoreTex = mFont.render(str(coins), False, (0, 0, 0))
            bMap = maps[current][:]
            dead = True
            xMapSize = mapWidths[current]*tileSize
            yMapSize = mapHeights[current]*tileSize
        else:
            scoreTex = mFont.render(str(coins), False, (0, 0, 0))
        coin=False
    
    camx = p1x
    camy = p1y
    onGround = False




    
    
def main():
    
    global mFont, scoreTex, black, grey, colors
    black = (0,0,0)
    grey = (0,0,90)
    white = (10, 10, 120)
    k = (20, 20, 240)
    n = (50,50,255)
    color = [black, grey, white, k, n]
    
    pygame.init()
    pygame.font.init()

    mFont = pygame.font.SysFont('Comic Sans MS', 48)
    scoreTex = mFont.render(str(coins), False, (0, 0, 0))
    
    pygame.key.set_repeat(10)
    global win
    win=pygame.display.set_mode((xWinSize,yWinSize),RESIZABLE)
    pygame.display.set_caption('A.I.D.S')

    global block1Tex
    block1Tex = pygame.image.load("blocks.png").convert()
    block1Tex = pygame.transform.scale(block1Tex, (tileSize*2, tileSize*2))
    global block2Tex
    block2Tex = pygame.image.load("blocks2.png").convert()
    block2Tex = pygame.transform.scale(block2Tex, (tileSize*2, tileSize*2))

    global blockTexes
    blockTexes = [block1Tex, block2Tex]

    while True:
        t0 = time.time()
        win.fill(color[current])
        
        handleEvents()
        update()
        drawMap()
        collision()
        drawPlayer()


        pygame.display.update()
        a = (time.time() - t0)
        if fps-a > 0:
            time.sleep(fps-a)

main()

