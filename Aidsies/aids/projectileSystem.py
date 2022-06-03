import sys, time, os
from MathMatrix import V2, Matrix2x2, Matrix2x2_t, make_rotation_Matrix_from_angle


class Projectile:
    pos = V2(50,50)
    speed = 0
    acc = 0
    vel = V2(1,0)
    MAX_SPEED = 10
    width = 500
    height = 500
    mapWidth = 30
    mapHeight = 30
    radius = 5
    dead = False
    blockSize = 32

    def __init__(self, x, y, radius=5, width=500, height=500, speed=0, acc=0, velx=11, vely=0):
        self.pos = V2(x, y)
        self.speed = speed
        self.acc = acc
        self.vel = V2(velx, vely)

    def setScreen(self, width, height):
        self.width = width
        self.height = height
        return self

    def setup(self, winWidth, winHeight, width, height, blockSize):
        self.width = width
        self.height = height
        self.mapWidth = width
        self.mapHeight = height
        self.blockSize = blockSize
        return self

    def die(self):
        self.dead = True

    def filterOffScreen(self):
        if self.pos.x < 0 or (self.pos.x-self.radius*0.5)/self.blockSize > self.mapWidth:
            self.die()
        if self.pos.y < 0 or (self.pos.y-self.radius*0.5)/self.blockSize > self.mapHeight:
            self.die()

    def updatePos(self):
        # checks if 
        if self.vel.getMagnitude() > self.MAX_SPEED+0.1:
            self.vel = self.vel.normalize().multByV1(self.MAX_SPEED)
            print("maxed")

        # move projectile
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.filterOffScreen()

    def setMaxSpeed(self, s):
        self.MAX_SPEED = s

    
class SpinningProj(Projectile):

    rotationAngle = 0
    R = Matrix2x2_t(0,0,0,0)
    constVel = V2(0,0)
    rotationIncrement = 0.1

    def __init__(self, x, y, rotationIncrement=0.1, rotationAngle=0, speed=0, acc=0, velx=0, vely=0):
        super().__init__(x, y, speed=0, acc=0, velx=0, vely=0)
        self.constVel = self.vel
        self.rotationAngle = rotationAngle
        self.rotationIncrement = rotationIncrement
        self.prepareR()

    def prepareR(self):
        #self.R = make_rotation_Matrix_from_angle(-self.rotationAngle)
        #self.rotate()
        pass

    def rotate(self, a, origin = 0):
        self.R = make_rotation_Matrix_from_angle(-a)
        self.vel = self.R.multByV2(self.constVel)
        self.vel.add(self.constVel.multByV1(0.5))
        self.rotationAngle += self.rotationIncrement

    def updatePos(self, a=0):
        self.rotate(self.rotationAngle)
        if self.constVel.getMagnitude() > self.MAX_SPEED+0.1:
            self.constVel = self.constVel.normalize().multByV1(self.MAX_SPEED)
        super().updatePos()