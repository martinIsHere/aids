import sys, time
import pygame
from pygame.locals import *

xWinSize = 1280
yWinSize = 700

#1280
#700

#xWinSize = int(input("x:"))
#yWinSize = int(input("y:"))

current = 0

maps = []
mapWidths = []
mapHeights = []
MAX_COINS_ARRAY = []

def loadMap(path):
    global mapWidths, mapHeights, maps, MAX_COINS_ARRAY
    file = open(path, "r")
    MAX_COINS_ARRAY.append(int(file.readline()))
    mapWidths.append(int(file.readline()))
    mapHeights.append(int(file.readline()))
    maps.append(list(file.readline()))
    file.close()

def loadMaps():
    loadMap("map1.txt")

    loadMap("map2.txt")

    loadMap("map3.txt")

    loadMap("map4.txt")

    loadMap("map5.txt")

    loadMap("map6.txt")

    loadMap("map7.txt")

    loadMap("map8.txt")

loadMaps()

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
vic = False # victory / hasWon
coin = False
animationTick = 0
buttonDown = False
bMenuState = False
bMainMenu = False


#Background image
BGSurface = pygame.Surface
BGSurfaceESC = pygame.Surface

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
maxSpeed = 7
s = maxSpeed
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
    else:
        return '0'

def getTile2(x,y):
    if x >= 0 and x < xMapSize and y >= 0 and y < yMapSize:
        return maps[current][int(y/tileSize)*mapWidths[current]+int(x/tileSize)]
    else:
        return '0'


def drawMap():
    global xVisibleTiles, yVisibleTiles, xOffset, yOffset, xMapSize, yMapSize, camx, camy, xGset, yGset, current, animationTick

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

            k=current%2
            
            if ID == '1':
                    win.blit(blockTexes[k], (bx, by), (0,0,tileSize,tileSize))
            elif ID == '2':
                    win.blit(blockTexes[k], (bx, by), (tileSize,0,tileSize,tileSize))
            elif ID == '3':
                    win.blit(blockTexes[k], (bx, by), (tileSize+(int(animationTick%4)*tileSize),
                                                       tileSize+(int(animationTick/4)*tileSize),
                                                       tileSize,tileSize))
            x+=1
        y+=1
        x=0
    y=0

def handleEvents():
    global current, startTime, velx, vely, s, onGround, jump, dead, pos, coin, coins, groundPoundSound, xNew, yNew, v, j, scoreTex, maps, bMap
    global mainLooping, bMenuState, buttonDown, bMainMenu
    
    vely = 1

    for event in pygame.event.get():
        
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

        #if in main loop check for input
        elif mainLooping:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    velx = 1
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    velx = -1
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if onGround:
                        jump = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    vely = 4
                elif event.key == pygame.K_r:
                    resetGame()
                    mainMenu()
                elif event.key == pygame.K_c:
                    x,y = pygame.mouse.get_pos()
                    setTile(int((x+xOffset)/tileSize),int((y+yOffset)/tileSize), '1')
                elif event.key == pygame.K_x:
                    x,y = pygame.mouse.get_pos()
                    setTile(int((x+xOffset)/tileSize),int((y+yOffset)/tileSize), '0')
                elif event.key == pygame.K_l:
                    coin = True
                    coins+=1
                elif event.key == pygame.K_LSHIFT:
                    s = int(maxSpeed/2)


            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if velx > 0:
                            velx = 0
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if velx < 0:
                            velx = 0
                    elif event.key == pygame.K_LSHIFT:
                        s = maxSpeed
                    elif event.key == pygame.K_ESCAPE:
                        mainLooping = False
                        menuState()
                    
        elif bMenuState or bMainMenu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttonDown = True

def drawPlayer():
    global xOffset, yOffset, p1x, p1y, velx, vely, current, playerTex, startTime, animationTick

    animationTick += 0.1
    
    p1x = xNew
    p1y = yNew
    #win.blit(blockTexes[current%2], (p1x-xOffset, p1y-yOffset), (0, tileSize, tileSize, tileSize))
    #pygame.draw.rect(win, (255, 0, 0), (p1x-xOffset, p1y-yOffset, 32, 32))
    win.blit(playerTex, (p1x-xOffset, p1y-yOffset), (int(animationTick%4)*32, int(animationTick/4)*32, 32,32))
    pygame.draw.rect(win, (0,0,255), (0,0,90,64))
    win.blit(scoreTex, (0,0))
    animationTick %= 7

    global timerText
    pygame.draw.rect(win, (255,255,255), (90,0,110,32))
    
    currentTime = int(time.time()-startTime)
    
    timerText = miniFont.render(str(int(currentTime/60)) + "m : " + str(currentTime%60) + "s", False, (0, 0, 0))
    win.blit(timerText, (90,0))
    
    #velx = 0
    #vely = 0

def collision():
    global velx, vely, p1x, p1y, tileSize, xNew, yNew, onGround, dead, jump, vic, coin, coins, v, j, headButt
    #left right
    if velx != 0:
        #right
        if velx > 0:
            topRight = getTile(int(xNew/tileSize+0.49), int(p1y/tileSize))
            bottomRight = getTile(int(xNew/tileSize+0.49), int(p1y/tileSize+0.49))
            
            if topRight == '1' or bottomRight == '1':
                xNew = int(xNew/tileSize)*tileSize+32

            elif topRight == '2' or bottomRight == '2':
                dead = True

            elif topRight == '3':
                setTile(int(xNew/tileSize+0.49), int(p1y/tileSize), '0')
                coin=True
                coins+=1
            elif bottomRight == '3':
                setTile(int(xNew/tileSize+0.49), int(p1y/tileSize+0.49), '0')
                coin=True
                coins+=1

        #left
        elif velx < 0:
            topLeft = getTile(int(xNew/tileSize), int(p1y/tileSize))
            bottomLeft = getTile(int(xNew/tileSize), int(p1y/tileSize+0.49))

            if topLeft == '1' or bottomLeft == '1':
                xNew = int(xNew/tileSize+1)*tileSize

            elif topLeft == '2' or bottomLeft == '2':
                dead = True

            elif topLeft == '3':
                setTile(int(xNew/tileSize), int(p1y/tileSize), '0')
                coin=True
                coins+=1
            elif bottomLeft == '3':
                setTile(int(xNew/tileSize), int(p1y/tileSize+0.49), '0')
                coin=True
                coins+=1
                
    #up down
    if vely != 0:
        #down
        if vely > 0:
            bottomLeft = getTile(int(xNew/tileSize), int(yNew/tileSize+0.49))
            bottomRight = getTile(int(xNew/tileSize+0.49), int(yNew/tileSize+0.49))
            
            if bottomLeft == '1' or bottomRight == '1':
                yNew = int(yNew/tileSize)*tileSize+32
                onGround = True

            elif bottomLeft == '2' or bottomRight == '2':
                dead = True

            elif bottomLeft == '3':
                setTile(int(xNew/tileSize), int(yNew/tileSize+0.49), '0')
                coin=True
                coins+=1
            elif bottomRight == '3':
                setTile(int(xNew/tileSize+0.49), int(yNew/tileSize+0.49), '0')
                coin=True
                coins+=1
            
        #up
        elif vely < 0:
            topLeft = getTile(int(xNew/tileSize), int(yNew/tileSize))
            topRight = getTile(int(xNew/tileSize+0.49), int(yNew/tileSize))
            
            if topLeft == '1' or topRight == '1':
                yNew = int(yNew/tileSize+1)*tileSize
                jump = False
                v = j
                headButt.play()

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
    global yMapSize, mapWidths, mapHeights, jumpSound, pickupSound, hurtSound, winSound, MAX_COINS_ARRAY
    xNew += velx*s
    #gravity
    if jump:
        vely = -1
        
        yNew += vely*v
        v-=(g/4)
        if v < 0:
            jump = False
            v = j
        if(onGround):
            jumpSound.play()
    else:
        yNew += vely*g

    if dead:
        hurtSound.play()
        dead = False
        xNew, yNew = m2p(1, 0)
        coins=0
        v = j
        scoreTex = mFont.render(str(coins)+"/" + str(MAX_COINS_ARRAY[current]), False, (255, 255, 0))
        maps[current] = bMap[:]
    elif coin:
        pickupSound.play()
        if coins >= MAX_COINS_ARRAY[current]:
            pickupSound.stop()
            winSound.play()
            
            if current < len(maps)-1:
                current+=1
            else:
                vic = True
                

            coins = 0
            scoreTex = mFont.render(str(coins)+"/" +str(MAX_COINS_ARRAY[current]), False, (255, 255, 0))
            bMap = maps[current][:]

            global BG_playlist
            BG_playlist[(current%(len(BG_playlist)+1))-1].stop()
            BG_playlist[current%(len(BG_playlist)+1)].stop()
            BG_playlist[current%(len(BG_playlist)+1)].play(-1)
            
            #Reset Player
            xNew, yNew = m2p(1, 0)
            coins=0
            xMapSize = mapWidths[current]*tileSize
            yMapSize = mapHeights[current]*tileSize
            v = j
            scoreTex = mFont.render(str(coins)+"/" + str(MAX_COINS_ARRAY[current]), False, (255, 255, 0))
    
        else:
            scoreTex = mFont.render(str(coins)+"/"+str(MAX_COINS_ARRAY[current]), False, (255, 255, 0))
        coin=False
    
    camx = p1x
    camy = p1y
    onGround = False



def load():
    global mFont, miniFont, scoreTex, colors, startTime, trueStartTime

    trueStartTime = time.time()
    startTime = trueStartTime;
    
    black = (0,0,0)
    grey = (0,0,90)
    white = (10, 10, 120)
    k = (20, 50, 80)
    n = (50,50,255)
    colors = [black, grey, white, k, n, white, black, k]
    
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    miniFont = pygame.font.Font("OpenSans-Light.ttf", 24)
    mFont = pygame.font.Font("OpenSans-Light.ttf", 48)
    scoreTex = mFont.render(str(coins)+"/" + str(MAX_COINS_ARRAY[current]), False, (255, 255, 0))

    # init sounds


    global hurtSound
    hurtSound = pygame.mixer.Sound("soundFX/Hit_Hurt.wav")
    hurtSound.set_volume(0.2)

    global pickupSound
    pickupSound = pygame.mixer.Sound("soundFX/Pickup_Coin.wav")
    pickupSound.set_volume(0.2)

    global winSound
    winSound = pygame.mixer.Sound("soundFX/win.wav")
    winSound.set_volume(0.2)

    global jumpSound
    jumpSound = pygame.mixer.Sound("soundFX/Jump.wav")
    jumpSound.set_volume(0.2)

    global headButt
    headButt = pygame.mixer.Sound("soundFX/Head_Butt.wav")
    

    global BG_playlist

    BG_playlist = [ pygame.mixer.Sound("soundFX/mainBGSong.wav"),
                    pygame.mixer.Sound("soundFX/SecondBGSong.wav"),
                    pygame.mixer.Sound("soundFX/ChillBGSong.wav"),
                    pygame.mixer.Sound("soundFX/ThirdBGSong.wav"),
                    pygame.mixer.Sound("soundFX/SickLoopBGSong.wav"),
                    pygame.mixer.Sound("soundFX/MehBGSong.wav"),
                    pygame.mixer.Sound("soundFX/FourthBGSong.wav"),
                    pygame.mixer.Sound("soundFX/soundTrapBGSong.mp3")
                    ]
    for sound in BG_playlist:
        sound.set_volume(0.2)
        
    BG_playlist[7].set_volume(0.4)
    
    BG_playlist[current%(len(BG_playlist)+1)].play(-1)
    
    pygame.key.set_repeat(10)
    
    global win, xWinSize, yWinSize
    win=pygame.display.set_mode((xWinSize,yWinSize))
    pygame.display.set_caption('A.I.D.S')

    global block1Tex
    block1Tex = pygame.image.load("blocks.png").convert_alpha()
    block2Tex = pygame.image.load("blocks2.png").convert_alpha()
    block2Tex = pygame.transform.scale(block2Tex, (160*2, 96*2))
    block1Tex = pygame.transform.scale(block1Tex, (160*2, 96*2))
    global playerTex
    playerTex = pygame.image.load("player.png").convert_alpha()
    

    global blockTexes
    blockTexes = [block1Tex, block2Tex]

    global frameDifference

    # https://www.beepbox.co/#9n31s6k0l00e0ft1La7g0fj07r1i0o432T0v1u00f50m92hc1ea2k02f3q8141d36w8h0E0T5v1ud3f10m8q011d23HVxh90000000000h0E0T3v1ud9f0q0x10l51d03SM005050wwpbaaihE1b2T2v1u15f10w4qw02d03w0E0b4h4y8ycPd4g14h0h4y8w0g00014h8y4g8y8h4jcPch8p234FH-470lQlidBcLEmyywFE5E8W1qa1qaa1o61waNoeAFFE-5tBt43lnnjllnjnhIox8RnmnXSUbLkTicBydbnnZsKDM3jbR_CwFH-47ljtnjppH-Fl53d7Fv8BCnBLp950Ak5IwgptwnJQ_0txH4idrrT3bRu10FEPxBT7dQ6nF7dM1PuAhMp7mhO17l8kAtp7mhw

    global BGSurface, tileSize, BGSurfaceESC
    BGSurface = pygame.Surface((xWinSize, yWinSize))
    BGSurfaceESC = pygame.Surface((xWinSize, yWinSize))
    tilesPerRow = xWinSize/tileSize
    tilesPerColumn = yWinSize/tileSize
    tilesOnScreen = (int)(tilesPerRow*tilesPerColumn)
    colorIncrease = 255/tilesOnScreen
    i = 0
    while(i <= tilesOnScreen+1):
        color = (int)(i*colorIncrease)
        if(color > 255):
            color = 255
        pygame.draw.rect(BGSurface, (color, 0, 0), ((i%tilesPerRow)*tileSize, (int)(i/tilesPerRow)*tileSize, tileSize, tileSize))
        pygame.draw.rect(BGSurfaceESC, (0, color, color), ((i%tilesPerRow)*tileSize, (int)(i/tilesPerRow)*tileSize, tileSize, tileSize))
        i+=1
    
    
    
def main():
    
    global mFont, miniFont, scoreTex, black, grey, colors, current, t0, vic

    global mainLooping
    mainLooping = True
    bMenuState = False
    bMainMenu = False
    
    
    while mainLooping:
        t0 = time.time()
        win.fill(colors[current])
        
        handleEvents()
        update()
        drawMap()
        collision()
        drawPlayer()

        pygame.display.update()
        frameDifference = (time.time() - t0)
        if fps-frameDifference > 0:
            time.sleep(fps-frameDifference)

        if vic:
            pauseTimer(t0)
        
    pygame.mixer.music.stop()
    

def pauseTimer(t0):
    global startTime
    startTime += time.time() - t0

def checkBtnCollision(x, y, w, h):
    mx, my = pygame.mouse.get_pos()
    if mx < x+w and mx > x and my < y+h and my > y:
        return True
    return False
    
def menuState():
    global win, color, fps, buttonDown, mainLooping, bMenuState, startTime, trueStartTime, miniFont
    global BGSurfaceESC

    buttonDown = False
    bMenuState = True
    mainLooping = False
    buttonText = mFont.render("Continue", False, (0, 255, 0))

    buttonWidth = 220
    buttonHeight = 100
    buttonX = (int)(xWinSize/4-(buttonWidth/4))
    buttonY = (int)(yWinSize/4-(buttonHeight/4))
    buttonColor = (255, 0, 0)
    
    while bMenuState:
        t0 = time.time()
        handleEvents()
        if buttonDown:
            #Continue Button
            if checkBtnCollision(buttonX, buttonY, buttonWidth, buttonHeight):
                bMenuState = False
                main()
                
        buttonDown = False
        win.blit(BGSurfaceESC, (0,0))
        
        pygame.draw.rect(win, buttonColor, (buttonX, buttonY, buttonWidth, buttonHeight), 5)
        win.blit(buttonText, (buttonX+10, buttonY+10))
        
        pygame.display.update()
        frameDifference = (time.time() - t0)
        if fps-frameDifference > 0:
            time.sleep(fps-frameDifference)
        pauseTimer(t0)



def resetGame():
    global startTime, trueStartTime
    startTime = time.time()
    trueStartTime = startTime

    global current, bMainMenu, bMenuState, mainLooping
    bMainMenu = False
    bMenuState = False
    mainLooping = False

    global buttonDown, xNew, yNew, p1x, p1y
    global camx, camy, velx, vely, maxSpeed, s, j, v, g, coins
    buttonDown = False
    xNew, yNew = m2p(1,0)
    p1x = 0
    p1y = 0
    camx = p1x
    camy = p1y
    velx = 0
    vely = 0
    maxSpeed = 7
    s = maxSpeed
    j = 25
    v = j
    g = 6
    coins = 0
    coin = False

    global BG_playlist
    BG_playlist[current].stop()

    global bMap, maps, xMapSize, yMapSize, scoreTex, mFont
    
    mapWidths.clear()
    mapHeights.clear()
    maps.clear()

    current = 0

    loadMaps()

    bMap = maps[current][:]
    
    xMapSize = mapWidths[current]*tileSize
    yMapSize = mapHeights[current]*tileSize
    
    scoreTex = mFont.render("0/7", False, (255, 255, 0))

    global vic
    vic = False

    

    load()

def mainMenu():
    global bMainMenu, bMenuState, mainLooping
    global xWinSize, yWinSize
    global buttonDown, startTime
    global BGSurface, tileSize
    
    bMainMenu = True
    bMenuState = False
    mainLooping = False

    buttonText = mFont.render("Start", False, (0, 255, 0))
    titleText = mFont.render("A.I.D.S.", False, (255, 255, 255))

    buttonWidth = 200
    buttonHeight = 100
    buttonX = xWinSize/2-(buttonWidth/2)
    buttonY = yWinSize/2-(buttonHeight/2)
    buttonColor = (255, 0, 0)

    while bMainMenu:
        t0 = time.time()
        handleEvents()
        if buttonDown:
            if checkBtnCollision(buttonX, buttonY, buttonWidth, buttonHeight):
                mainLooping = True
                bMainMenu = False
                main()
        buttonDown = False
        win.blit(BGSurface, (0,0))
        
        pygame.draw.rect(win, buttonColor, (buttonX, buttonY, buttonWidth, buttonHeight), 5)
        win.blit(buttonText, (buttonX+10, buttonY+10))
        
        pygame.display.update()
        frameDifference = (time.time() - t0)
        if fps-frameDifference > 0:
            time.sleep(fps-frameDifference)
        startTime += time.time() - t0

#Main sequence
load()
mainMenu()
main()

