import random
import pygame
from pygame import *

pygame.init()
# встановлуємо задній фон
window = display.set_mode((1000, 800))
background = image.load('res2/cosmos.jpg')
# scale - змінити розмір   (картинка, (ширина, висота))
background = transform.scale(background, (1000, 800))
# змінна для таймера та житті
clock = time.Clock()
helth = 10
# робимо клас спрайт з базовими


class Sprite(sprite.Sprite):

    def __init__(self, filename, x, y, wight=120, height=120, speed=0, lifes=0):
        super().__init__()
        self.image = transform.scale(image.load(filename), (wight, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = speed
        self.lifes = lifes

    # малюю
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# клас гравець
class Player(Sprite):

    def update(self):
        pressed_keys = key.get_pressed()
        if pressed_keys[K_a]:
            self.rect.x -= self.speed
        if pressed_keys[K_d]:
            self.rect.x += self.speed


# клас спрайт
class Ufo(Sprite):
    def update(self,):
        self.rect.y += self.speed
        if self.rect.y > window.get_height():  # перевірити чи тарілка нижче за кординату вікна
            # знищити спрайт
            spa_boat.lifes -= 1
            self.kill()


# клас снаряда
class Bulet(Sprite):
    def update(self):
        self.rect.y -= self.speed


def label(text, size, label_font, color, x, y):
    # Створити шрифт
    new_font = font.SysFont(label_font, size)
    # На основі шрифта створити текст
    text = new_font.render(text, True, (100, 100, 100))
    # намалювати текст
    window.blit(text, (x, y))
# спавнимо космічні тарілки
spa_enemy0 = Ufo('res2/spase_bot.png', 440, 200, wight=120, height=90, speed=1)
spa_enemy1 = Ufo('res2/spase_bot.png', 440, 200, wight=120, height=90, speed=1)
spa_enemy2 = Ufo('res2/spase_bot.png', 440, 200, wight=120, height=90, speed=1)

you_lose = image.load('res2/you_lose.png')
you_lose = transform.scale(you_lose, (300, 200))
you_win = image.load('res2/you_win.png')
you_win = transform.scale(you_win, (220, 150))
# робимо групи
ufos = sprite.Group()
bulets = sprite.Group()
spa_boat = Player('res2/cosmos_boat_crafting.png', 440, 650, speed=5, lifes=10)
game_skore = 0
# починає цикл
sped_plus = 2
sped_skore = 30
game = True
run = True
while game:
    while len(ufos) < 7:
        new_ufo = Ufo('res2/spase_bot.png', random.randint(0, window.get_width() - 100), -100, 100, 50, 1)
        ufos.add(new_ufo)
    # event.get() - отримати події
    # for e in event.get() - для кожної події, яка зараз відбувається
    for e in event.get():
        # якщо тип події - вийти
        if e.type == QUIT:
            game = False  # завершити цикл
        # перевіряємо чи натиснуто 1 раз
        if e.type == KEYDOWN:
            if e.key == K_w:
                bulets.add(Bulet('res2/bullet.png', spa_boat.rect.x + 55, spa_boat.rect.y, 10, 30, 5))
        #if e.type == MOUSEBUTTONDOWN:

    if run:
        # дати значення якщо житті закінчилися поразка
        # якщо набрав 1000 очок перемога
        if spa_boat.lifes == 0:
            run = False
        if game_skore >= 1000:
            run = False
        window.blit(background, (0, 0))
        # намалювати космічний кoрабель
        spa_boat.draw()
        spa_boat.update()
        if game_skore == sped_skore:
            for ufo in ufos:
                ufo.speed += sped_plus
            sped_skore += random.randint(20, 50)

        interaction = sprite.groupcollide(bulets, ufos, True, True)
        for bulet in interaction:
            game_skore += len(interaction[bulet])
        # намалювати снаряд
        bulets.update()
        bulets.draw(window)
        # намалювати космічні тарілки
        ufos.update()
        ufos.draw(window)
        label('рахунок ' + str(game_skore), 40, 'Montserrat', (100, 100, 100), 0, 10)
        label('житті ' + str(spa_boat.lifes), 40, 'Montserrat', (100, 100, 100), 0, 40)
    elif game_skore >= 1000:
        window.blit(you_win, (window.get_width() / 2 - you_win.get_width() / 2, window.get_height() / 2 - you_win.get_height() / 2))
    else:
        window.blit(you_lose, (window.get_width() / 2 - you_lose.get_width() / 2, window.get_height() / 2 - you_lose.get_height() / 2))
    # намалювати вікно
    display.update()
    clock.tick(60)
