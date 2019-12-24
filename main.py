import random
import tkinter as tk
from tkinter import messagebox
import pygame

pygame.init()
pygame.font.init()
S_COLOR = (48, 77, 219, 100)
FOOD_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ICON = pygame.image.load('img/snake.ico')
BGIMG = pygame.image.load("img/grassboard.png")

WIDTH = 500
ROWS = 20
gameScreen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Snakey Snake!')
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()
gameOver = False


class Circle(object):
    rows = 20
    w = 500

    def __init__(self, start, dirX=1, dirY=0, color=S_COLOR):
        self.pos = start
        self.dirX = 1
        self.dirY = 0
        self.color = color

    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)

    def draw(self, surface, showEyes=False):
        dist = self.w // self.rows
        radius = 11
        x = self.pos[0]
        y = self.pos[1]

        pygame.draw.circle(surface, self.color,
                           ((x * dist) + radius + 1, (y * dist) + radius + 1), radius)

        if showEyes:
            centre = dist // 2
            r = 3
            eye1 = (x * dist + centre - (r + 1), y * dist + 8)
            eye2 = (x * dist + dist - (r * 2) - 1, y * dist + 8)
            pygame.draw.circle(surface, WHITE, eye1, r)
            pygame.draw.circle(surface, WHITE, eye2, r)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Circle(pos)
        self.body.append(self.head)
        self.dirX = 0
        self.dirY = 1

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dirX = 0
            self.dirY = -1
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dirX = 0
            self.dirY = 1
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dirX = -1
            self.dirY = 0
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dirX = 1
            self.dirY = 0
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        for index, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if index == len(self.body) - 1:
                    self.turns.pop(p)

            else:
                if c.dirX == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirX == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                elif c.dirY == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                else:
                    c.move(c.dirX, c.dirY)

    def reset(self, pos):
        self.head = Circle(pos)
        self.body = []
        self.turns = {}
        self.dirX = 0
        self.dirY = 1
        self.body.append(self.head)

    def addCircle(self):
        tail = self.body[-1]
        tailX, tailY = tail.dirX, tail.dirY

        if tailX == -1 and tailY == 0:
            self.body.append(Circle((tail.pos[0] + 1, tail.pos[1])))
        elif tailX == 1 and tailY == 0:
            self.body.append(Circle((tail.pos[0] - 1, tail.pos[1])))
        elif tailX == 0 and tailY == -1:
            self.body.append(Circle((tail.pos[0], tail.pos[1] + 1)))
        elif tailX == 0 and tailY == 1:
            self.body.append(Circle((tail.pos[0], tail.pos[1] - 1)))

        self.body[-1].dirX = tailX
        self.body[-1].dirY = tailY

    def draw(self, surface):
        for index, c in enumerate(self.body):
            if index == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def updateScreen(surface):
    global S, food, paused
    surface.blit(BGIMG, (0, 0))
    S.draw(surface)
    food.draw(surface)
    pygame.display.update()


def fade(width, height):
    global paused
    fade = pygame.Surface((width, height))
    fade.fill((255, 255, 255))
    for alpha in range(20):
        fade.set_alpha(alpha)
        gameScreen.blit(fade, (25, 25))
        pausedMenu((204, 50, 50))
        pygame.display.update()
        pygame.time.delay(5)


def showText(fontStyle, fontSize, text, color, ySpacing):
    myFont = pygame.font.SysFont(fontStyle, fontSize)
    label = myFont.render(text, 2, color)
    labelRect = label.get_rect(center=(WIDTH // 2, WIDTH // 8 + ySpacing))
    gameScreen.blit(label, labelRect)


def pausedMenu(col):
    showText("comicsansms", 55, "Snakey Snake!", col, 50)
    showText("comicsansms", 40, "Press:", col, 150)
    showText("comicsansms", 30, "'Spacebar' - Play / Pause", col, 200)
    showText("comicsansms", 30, "'Esc' - Play / Pause", col, 250)
    showText("comicsansms", 30, "'Q' - Quit Game", col, 300)


def randomFood(r, snake):
    while True:
        x = random.randrange(r)
        y = random.randrange(r)

        # filter to prevent food from generating on top of the snake
        if len(list(filter(lambda snk: snk.pos == (x, y), snake.body))) > 0:
            continue
        else:
            break
    return (x, y)


def msgBox(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def mainLoop():
    global WIDTH, ROWS, gameScreen, gameOver, S, food, paused
    paused = True

    S = Snake((0, 255, 0), (12, 12))
    food = Circle(randomFood(ROWS, S), 0, 0, FOOD_COLOR)
    gameScreen.blit(BGIMG, (0, 0))
    fade(WIDTH - 50, WIDTH - 50)

    while not gameOver:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameOver = True
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    paused = not paused
                    fade(WIDTH - 50, WIDTH - 50)

        clock.tick(8)
        if not paused:
            S.move()

            if S.body[0].pos == food.pos:
                S.addCircle()
                food = Circle(randomFood(ROWS, S), 0, 0, FOOD_COLOR)

            for i in range(len(S.body)):
                if S.body[i].pos in list(map(lambda sk: sk.pos, S.body[i+1:])):
                    msgBox('Game Over!',
                           f'Your Score: {str(len(S.body))}\nPlay again...')
                    S.reset((10, 10))
                    break

            updateScreen(gameScreen)


mainLoop()
pygame.quit()
