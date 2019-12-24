import random
import pygame

pygame.init()
pygame.font.init()

# Global Colors and Images
S_COLOR = (15, 119, 220)
FOOD_COLOR = (214, 70, 62)
TXT_COLOR = (204, 50, 50)
WHITE = (255, 255, 255)
ICON = pygame.image.load('img/snake.ico')
BGIMG = pygame.image.load("img/grassboard.png")
TITLE = 'Slithering Snake!'

# Initialize Game Vars
WIDTH = 500
ROWS = 20
gameScreen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption(TITLE)
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


def showMenu(width, height, txtFunc):
    global paused
    menuBox = pygame.Surface((width, height))
    menuBox.fill(WHITE)
    for alpha in range(21):
        menuBox.set_alpha(alpha)
        gameScreen.blit(menuBox, (25, 25))
        txtFunc()
        pygame.display.update()
        pygame.time.delay(5)


def showText(fontStyle, fontSize, text, color, ySpacing):
    myFont = pygame.font.SysFont(fontStyle, fontSize)
    label = myFont.render(text, 2, color)
    labelRect = label.get_rect(center=(WIDTH // 2, WIDTH // 8 + ySpacing))
    gameScreen.blit(label, labelRect)


def pausedMenu(col):
    iconRect = ICON.get_rect(center=(WIDTH // 2, 80))
    gameScreen.blit(ICON, iconRect)
    showText("comicsansms", 50, TITLE, (14, 158, 67), 90)
    showText("comicsansms", 40, "--------------------", col, 130)
    showText("comicsansms", 40, "Press:", col, 170)
    showText("comicsansms", 30, "'Arrow Keys' - Move Snake", col, 220)
    showText("comicsansms", 30, "'Esc' / 'Space' - Play / Pause", col, 270)
    showText("comicsansms", 30, "'Q' - Quit Game", col, 320)


def gameOverMenu(col, score):
    showText("comicsansms", 50, TITLE, (14, 158, 67), 10)
    showText("comicsansms", 40, "* Game Over *", col, 100)
    showText("comicsansms", 40, f"Your Score: {score}", col, 160)
    showText("comicsansms", 30, "'Arrow Keys' - Move Snake", col, 230)
    showText("comicsansms", 30, "'Esc' / 'Space' - Play / Pause", col, 270)
    showText("comicsansms", 30, "'Q' - Quit Game", col, 310)


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


def mainLoop():
    global WIDTH, ROWS, gameScreen, gameOver, S, food, paused
    paused = True

    S = Snake((0, 255, 0), (12, 12))
    food = Circle(randomFood(ROWS, S), 0, 0, FOOD_COLOR)
    gameScreen.blit(BGIMG, (0, 0))
    showMenu(WIDTH - 50, WIDTH - 50, lambda: pausedMenu(TXT_COLOR))

    while not gameOver:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameOver = True
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        showMenu(WIDTH - 50, WIDTH - 50,
                                 lambda: pausedMenu(TXT_COLOR))

        if not paused:
            clock.tick(8)
            S.move()

            if S.body[0].pos == food.pos:
                S.addCircle()
                food = Circle(randomFood(ROWS, S), 0, 0, FOOD_COLOR)

            updateScreen(gameScreen)

            for i in range(len(S.body)):
                # Check if snake collides with its body
                if S.body[i].pos in list(map(lambda sk: sk.pos, S.body[i + 1:])):
                    paused = True
                    showMenu(WIDTH - 50, WIDTH - 50,
                             lambda: gameOverMenu(TXT_COLOR, str(len(S.body))))
                    S.reset((10, 10))
                    break


mainLoop()
pygame.quit()
