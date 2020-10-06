import pygame
import os
import random as r
import time

# initializing pygame
pygame.init()

#clock
clock = pygame.time.Clock()

#window size
winX = 780 + 10 + 10
winY = 780 + 60 + 10

# creating window surface
win = pygame.display.set_mode((winX, winY))
pygame.display.set_caption('Snake Game')

#Score Variable
score = 0
font = pygame.font.SysFont('comicsans',35,1)

#size of square = 26
# GRID is 30x30

#creates a list with all possible X and Y within the grid
i=30
Xvalue = 10
Yvalue = 60
allX = []
allY = []
while i > 0:
    allX.append(Xvalue)
    Xvalue += 26
    allY.append(Yvalue)
    Yvalue += 26
    i -= 1

# list that will house the body lenth and place in the grid
snakeBody = []

# -------------------------------------------------

class Boundary:
    '''class to make boundaries'''

    def __init__(self, x,width,y,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,win):
        pygame.draw.rect(win,(0,0,0),(self.x, self.y, self.width, self.height))

class Apple:

    def __init__(self,x,y):
        self.x = allX[x-1]
        self.y = allY[y-1]
        self.yes = True

    def draw(self,win):
        # pygame.draw.rect(win,(255,0,0),(self.x, self.y, 26, 26))
        pygame.draw.circle(win,(255,0,0),(int(self.x+26/2), int(self.y+26/2)),int(10))

    def newSpace(self):
        '''Moves apple to a randome spot in the grid'''
        self.x = allX[r.randint(0, len(allX)-1)]
        self.y = allY[r.randint(0, len(allY)-1)]
        self.yes = True
        while self.yes:
            for body in snakeBody:
                if self.x == body[0]:
                    if self.y == body[1]:
                        self.x = allX[r.randint(0, len(allX) - 1)]
                        self.y = allY[r.randint(0, len(allY) - 1)]
                        print('BALL SPAWN ON SNAKE')
                    else:
                        self.yes = False
                else:
                    self.yes = False

class Snake:

    def __init__(self,startX, startY):
        self.x = allX[startX]
        self.y = allY[startY]
        self.square = 26
        self.tick = 0
        self.speed = 250
        self.Vel = 1
        self.isMovingX = True
        self.isMovingY = False
        self.hit = False
        snakeBody.append((self.x, self.y))
        snakeBody.append((self.x, self.y))

    def draw(self, win):
        pygame.draw.rect(win,(0,0,0),(self.x, self.y, self.square, self.square),5)
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.square, self.square))

    def move(self):

        #seting a clock for the moving speed
        if self.tick >= 1 and self.tick < self.speed:
            self.tick += 1
        else:
            self.tick = 0

        self.eat()      #checking if ate an apple
        keys = pygame.key.get_pressed()
        # set a constant move
        if self.isMovingX:
            if self.tick == 0 and 0 <= allX.index(self.x) < 30:
                if allX.index(self.x) < 29:
                    self.x = allX[allX.index(self.x)+self.Vel]
                    self.tick = 1
                elif allX.index(self.x) == 29:
                    if self.Vel == -1:
                        self.x = allX[allX.index(self.x)+self.Vel]
                        self.tick = 1
                    elif self.Vel == 1:
                        self.x = allX[0]
                        self.tick = 1

        if self.isMovingY:
            if self.tick == 0 and 0 <= allY.index(self.y) < 30:
                if allY.index(self.y) < 29:
                    self.y = allY[allY.index(self.y)+self.Vel]
                    self.tick = 1
                elif allY.index(self.y) == 29:
                    if self.Vel == -1:
                        self.y = allY[allY.index(self.y) + self.Vel]
                        self.tick = 1
                    else:
                        self.y = allY[0]
                        self.tick = 1



        # checking for key press and changing the direction

        if keys[pygame.K_RIGHT]:
            self.isMovingX = True
            self.isMovingY = False
            self.Vel = 1
        if keys[pygame.K_LEFT]:
            self.isMovingX = True
            self.isMovingY = False
            self.Vel = -1
        if keys[pygame.K_UP]:
            self.isMovingX = False
            self.isMovingY = True
            self.Vel = -1
        if keys[pygame.K_DOWN]:
            self.isMovingX = False
            self.isMovingY = True
            self.Vel = 1

    def eat(self):
        ''' Checks if ate an apple '''
        if self.tick == 0:
            snakeBody.append((self.x, self.y))
            if self.x == apple.x and self.y == apple.y:
                apple.newSpace()
                if self.speed > 50:
                    self.speed -= 10
                else:
                    self.speed -= 2
                global score
                score += 1
            else:
                del snakeBody[0]
            # print('---------------')
            # print(self.x, apple.x)
            # print(self.y, apple.y)

    def gameOver(self):
        '''resets everything'''
        if self.tick <= 1:
            pause()
        global snakeBody, score
        score = 0
        snakeBody = []
        self.x = allX[15]
        self.y = allY[15]
        self.speed = 250
        self.isMovingX = True
        self.isMovingY = False
        self.hit = False
        snakeBody.append((self.x, self.y))



# -------------------------------------------------

def snakeColide():
        for body in snakeBody:
            if snake.x == body[0] and snake.y == body[1]:
                snake.gameOver()

def draw():

    #White backround
    win.fill((255, 255, 255))

    #Drawing walls
    for wall in walls:
        wall.draw(win)

    #Printing score
    text = font.render('Score:  '+str(score),1,(0,0,0))
    win.blit(text,(int(winX/2-text.get_width()/2), int(30-text.get_height()/2)))

    #drawing apple
    apple.draw(win)

    for part in snakeBody:
        pygame.draw.rect(win,(0,0,0),(part[0],part[1],26,26),5)
        pygame.draw.rect(win, (0, 0, 0), (part[0], part[1], 26, 26))

    # drawing Head of snake
    snake.draw(win)

    pygame.display.update()

def mainLoop():
    run = True
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if keys[pygame.K_ESCAPE]:
            run = False
        if keys[pygame.K_SPACE]:
            pass

        snake.move()
        draw()
        snakeColide()

    pygame.quit()

def pause():

    run = False
    while not(run):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        if keys[pygame.K_SPACE]:
            run = True

        global score
        win.fill((255, 255, 255), (10, 60, 780, 780))
        font = pygame.font.SysFont('comicsans', 50, 1)
        gameOver_text = font.render('GAME OVER', 1, (255, 0, 0))
        finalScore_text = font.render('Your score: ' + str(score), 1, (255, 0, 0))
        pressSpace = font.render('[press space to play again]', 1, (0, 0, 0))

        win.blit(gameOver_text,
                 (int(winX / 2 - gameOver_text.get_width() / 2), int(winY / 2 - gameOver_text.get_height() / 2) - 30))
        win.blit(finalScore_text,
                 (int(winX / 2 - finalScore_text.get_width() / 2), int(winY / 2 - finalScore_text.get_height() / 2) + 30))
        win.blit(pressSpace,
                 (int(winX / 2 - pressSpace.get_width() / 2), int(winY - 10 - 20 - pressSpace.get_height() / 2 - 20)))

        pygame.display.update()
        clock.tick(15)


# -------------------------------------------------

#Drawing boundaries
topWall = Boundary(0, 800, 0, 10)
top2Wall = Boundary(0, 800, 50, 10)
bottomWall = Boundary(0, 800, 840, 10)
leftWall = Boundary(0, 10, 0, winY)
rightWall = Boundary(790, 10, 0, winY)

walls = [topWall, top2Wall, bottomWall, leftWall, rightWall]

#creating apple
apple = Apple(15,15)

#creating snake
snake = Snake(20,3)

# -------------------------------------------------

mainLoop()
