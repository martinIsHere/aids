import pygame, sys, time
from pygame.locals import *


xWinSize = 1100
yWinSize = 700


fps = 1/60
tileSize = 32*2
mapHeight = 31
mapWidth = 44
xMapSize = mapWidth*tileSize
yMapSize = mapHeight*tileSize
xVisibleTiles = xWinSize/tileSize+1
yVisibleTiles = yWinSize/tileSize+1
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
clip = False


def m2p(x, y):
    if x >= 0 and x < mapWidth and y >= 0 and y < mapHeight:
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
s = 8
j = 20
v = j
g = 4
coins = 0

a=0
b=0
file = open("map2.txt", 'r+')
#while a < mapHeight:
#    while b < mapWidth:
#        file.write(map1[a*mapWidth+b])
#        
#        
#        b+=1
#    a+=1
#    b=0

map2 = list("")
for ch in file:
    map2 += ch
file.close()

bMap = map2[:]

def getTile(x, y):
    if x >= 0 and x < mapWidth and y >= 0 and y < mapHeight:
        return map2[y * mapWidth + x]
    else:
        return '0'

def setTile(x, y, i):
    if x >= 0 and x < mapWidth and y >= 0 and y < mapHeight:
        map2[y * mapWidth + x] = i

def getTile2(x,y):
    if x >= 0 and x < xMapSize and y >= 0 and y < yMapSize:
        return map2[int(y/tileSize)*mapWidth+int(x/tileSize)]
    else:
        return 0



def drawMap():
    global xVisibleTiles, yVisibleTiles, xOffset, yOffset, xMapSize, yMapSize, camx, camy, xGset, yGset

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
                    win.blit(block1Tex, (bx, by), (0,0,tileSize,tileSize))
            elif ID == '2':
                    win.blit(block1Tex, (bx, by), (tileSize,0,tileSize,tileSize))
            elif ID == '3':
                    win.blit(block1Tex, (bx, by), (tileSize,tileSize,tileSize,tileSize))
            x+=1
        y+=1
        x=0
    y=0

def handleEvents():
    global velx, vely, s, onGround, jump, dead, pos, clip, map1

    if (clip):
        vely = 1
    else:
        vely = 0

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
                vely = -1
            elif event.key == pygame.K_s:
                vely = 1
            elif event.key == pygame.K_r:
                dead = True
            elif event.key == pygame.K_c:
                x,y = pygame.mouse.get_pos()
                setTile(int((x+xOffset)/tileSize),int((y+yOffset)/tileSize), '1')
            elif event.key == pygame.K_v:
                x,y = pygame.mouse.get_pos()
                setTile(int((x+xOffset)/tileSize),int((y+yOffset)/tileSize), '2')
            elif event.key == pygame.K_b:
                x,y = pygame.mouse.get_pos()
                setTile(int((x+xOffset)/tileSize),int((y+yOffset)/tileSize), '3')
            elif event.key == pygame.K_n:
                x,y = pygame.mouse.get_pos()
                setTile(int((x+xOffset)/tileSize),int((y+yOffset)/tileSize), '0')
            elif event.key == pygame.K_p:
                file = open("map2.txt", 'w')
                for a in map2:
                    file.write(a)
                file.close()


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                if velx > 0:
                    velx = 0
            elif event.key == pygame.K_a:
                if velx < 0:
                    velx = 0
            elif event.key == pygame.K_j:
                if clip:
                    clip = False
                else:
                    clip = True

def drawPlayer():
    global xOffset, yOffset, p1x, p1y, velx, vely
    p1x = xNew
    p1y = yNew
    win.blit(block1Tex, (p1x-xOffset, p1y-yOffset), (0, tileSize, tileSize, tileSize))
    pygame.draw.rect(win, (255,255,255), (0,0,50,40))
    win.blit(scoreTex, (0,0))
    #velx = 0
    

def collision():
    global velx, vely, p1x, p1y, tileSize, xNew, yNew, onGround, dead, jump, vic, coin, coins
    #left right
    if velx != 0:
        #right
        if velx > 0:
            topRight = getTile(int(xNew/tileSize+0.99), int(p1y/tileSize))
            bottomRight = getTile(int(xNew/tileSize+0.99), int(p1y/tileSize+0.99))
            
            if topRight == '1' or bottomRight == '1':
                xNew = int(xNew/tileSize)*tileSize


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

            elif topLeft == '3':
                setTile(int(xNew/tileSize), int(yNew/tileSize), '0')
                coin=True
                coins+=1
            elif topRight == '3':
                setTile(int(xNew/tileSize+0.99), int(yNew/tileSize), '0')
                coin=True
                coins+=1
                
  
               

def update():
    global xNew, yNew, velx, vely, camx, camy, p1x, p1y, onGround, jump, v, dead, vic, map2, bMap, coins, coin, scoreTex, mFont, j, clip
    xNew += velx*s
    if not clip:
        yNew += vely*s
    #gravity
    if jump:
        vely = -1
        
        yNew += vely*v
        v-=(g/4)
        if v < 0:
            jump = False
            v = j
    else:
        if clip:
            yNew += vely*g
        

    if dead:
        dead = False
        print("Dead!")
        coins=0
        scoreTex = mFont.render(str(coins), False, (0, 0, 0))
        map2 = bMap[:]
    elif coin:
        scoreTex = mFont.render(str(coins), False, (0, 0, 0))
        coin=False
    elif coins >= 7:
        print("Win!")
        coins=0
    
    
    camx = p1x
    camy = p1y
    onGround = False
    
def main():

    global mFont, scoreTex, clip
    
    pygame.init()
    pygame.font.init()

    mFont = pygame.font.SysFont('Comic Sans MS', 30)
    scoreTex = mFont.render(str(coins), False, (0, 0, 0))
    
    pygame.key.set_repeat(10)
    global win
    win=pygame.display.set_mode((xWinSize,yWinSize),0,32)
    pygame.display.set_caption('A.I.D.S')

    global block1Tex
    block1Tex = pygame.image.load("blocks.png").convert()
    block1Tex = pygame.transform.scale(block1Tex, (tileSize*2, tileSize*2))

    while True:
        t0 = time.time()
        win.fill((0,0,0))
        
        handleEvents()
        update()
        drawMap()
        if clip:
            collision()
        drawPlayer()


        pygame.display.update()
        a = (time.time() - t0)
        if fps-a > 0:
            time.sleep(fps-a)

main()

