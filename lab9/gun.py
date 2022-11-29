import math
from random import choice
from random import randint
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
s1, s2 = '', ''
points = 0


def text():
    global points, s1
    s1 = 'Scores: ' + str(points)
    f1 = pygame.font.Font(None, 30)
    text1 = f1.render(s1, True, BLACK)
    screen.blit(text1, (15, 50))


def text2():
    global bullet, s2
    s2 = 'You destroyed the target in ' + str(bullet) + ' shots'
    f2 = pygame.font.Font(None, 30)
    text1 = f2.render(s2, True, BLACK)
    screen.blit(text1, (250, 300))


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.y - self.vy + self.r > HEIGHT and self.vy < 0:
            self.vy = -self.vy * 0.6
            self.vx = self.vx * 0.5
            if -0.0001 < self.vx < 0.0001:
                self.r = 0
        elif self.y - self.vy < self.r > 0:
            self.vy = -self.vy
        else:
            self.vy += -1
        if (self.x + self.vx + self.r > WIDTH and self.vx > 0) or (self.x + self.vx - self.r < 0 and self.vx < 0):
            self.vx = -self.vx * 0.8
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r, 1
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        dx = self.x - obj.x
        dy = self.y - obj.y
        dr = (dx**2 + dy**2)**0.5
        if dr <= obj.r + self.r:
            return True
        else:
            return False


class AngryBall(Ball):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 7
        self.vx = 0
        self.vy = 0
        self.color = GREEN
        self.live = 30


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        tip = randint(0, 5)
        if tip == 0:
            new_ball = AngryBall(self.screen)
        else:
            new_ball = Ball(self.screen)
            new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        if tip == 0:
            new_ball.vx = new_ball.vx * 8
            new_ball.vy = new_ball.vy * 8
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0]-20) == 0:
                self.an = - math.pi / 2
            else:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))

        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        x1 = 20 + 5 * math.sin(self.an)
        y1 = 450 - 5 * math.cos(self.an)

        x2 = 20 - 5 * math.sin(self.an)
        y2 = 450 + 5 * math.cos(self.an)

        k = (self.f2_power - 10) / 90

        dx = (20 + 100 * k) * math.cos(self.an)
        dy = (20 + 100 * k) * math.sin(self.an)

        pygame.draw.polygon(self.screen, self.color, [[x2, y2], [x1, y1], [x1 + dx, y1 + dy], [x2 + dx, y2 + dy]])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 50)
        self.color = RED
        self.vy = randint(0, 5)
        self.vx = randint(0, 5)
        self.live = 1

    def hit(self):
        """Попадание шарика в цель."""
        global points
        points += 1

    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK,
                           (self.x, self.y), self.r, 1)

    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям окна (размер окна 800х600).
        """
        if (self.y - self.vy + self.r > HEIGHT and self.vy < 0) or (self.y - self.vy < self.r > 0):
            self.vy = -self.vy
        if (self.x + self.vx + self.r > WIDTH and self.vx > 0) or (self.x + self.vx - self.r < 0 and self.vx < 0):
            self.vx = -self.vx
        self.x += self.vx
        self.y -= self.vy


class AngryTarget(Target):
    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK,
                           (self.x, self.y), self.r, 1)
        pygame.draw.circle(self.screen, BLUE,
                           (self.x, self.y), self.r/2)

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 50)
        self.color = RED
        self.vy = randint(5, 50)
        self.vx = randint(5, 50)
        self.live = 1


def draw_all():
    global balls, targets, gun
    gun.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()


def move_and_hit():
    global targets, balls, a
    for t in targets:
        t.move()
        for b in balls:
            b.move()
            if b.hittest(t) and t.live:
                t.live = 0
                t.hit()
                balls = []
                t.new_target()
                a = True


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
a = False

text()
text2()
clock = pygame.time.Clock()
gun = Gun(screen)
targets = [AngryTarget(screen), Target(screen), Target(screen)]
finished = False

while not finished:
    screen.fill(WHITE)
    text()
    draw_all()
    if a:
        text2()
        bullet = 0
    pygame.display.update()
    if a:
        a = False
        clock.tick(0.8)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    move_and_hit()
    gun.power_up()
pygame.quit()
