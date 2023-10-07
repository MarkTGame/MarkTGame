import mixer as mixer
import pygame.font
from pygame import *
from random import *

FPS  = 60

mixer.init()

mixer.music.load('Sprite/space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('Sprite/fire.ogg')

background_image = "galaxy.jpg"
hero_image = "Sprite/rocket.png"
bullet_image = "Sprite/bullet.png"

pygame.font.init()

font1 = font.SysFont('Arial', 50)
font2 = font.SysFont('Arial', 30)
font3 = font.SysFont('Arial', 70)

win = font1.render("YOU WIN!", True, (0,255,0))
lose = font1.render("YOU LOSE!", True, (255,0,0))
reload = font2.render("For reload game push esc",True, (255,0,0))

reload_rect = reload.get_rect(topleft=(180, 200))




window_width = 700

window_height = 500

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, side = 0):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.side = side

    def coliderect(self, rect):
        return self.rect.coliderect(rect)


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


index_color = 0


class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):

    def update(self):

        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < window_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()

        if keys[K_ESCAPE] and self.rect.x > 5:
            self.rect.x -= self.speed














    def fire(self):

        bullet = Bullet(bullet_image,self.rect.centerx, self.rect.top, 15, 20, 3)
        bullets.add(bullet)








destroyed_ships = 0
bullets = sprite.Group()
lost = 0

class Enemy(GameSprite):


    def update(self):

        global destroyed_ships, lost

        self.rect.y += self.speed

        if self.side != 1:
            if self.rect.x > 30:
                self.rect.x -= self.speed

            if self.rect.x == 40:
                self.side = 1

        if self.side != 2:
            if self.rect.x < window_width - 50:
                self.rect.x += self.speed

            if self.rect.x == window_width - 100:
                self.side = 2

        if self.rect.y > window_height:
            self.rect.x = randint(80, window_width - 80)
            self.rect.y = 0
            lost += 1





monsters = sprite.Group()

asteroids = sprite.Group()

hp = 5

def create_asteroids(asteroid=None, asteroids=None):
    asteroid = Enemy("Sprite/asteroid.png", randint(80, window_width - 80), -40, 80, 50, 1, randint(1, 2))
    asteroids.add(asteroid)


def create_monster():
    monster = Enemy("Sprite/ufo.png", randint(80, window_width - 80), -40, 80, 50, 1, randint(1, 2))
    monsters.add(monster)

for i in range(3):
    create_monster()

for i in range(1):
    create_monster()
for i in range(5):
    monster = Enemy("Sprite/ufo.png", randint(80, window_width - 80), -40, 80, 50, 1, randint(1, 2))
    monsters.add(monster)

window = display.set_mode((window_width, window_height))

background = transform.scale(image.load(background_image), (window_width, window_height))

ship = Player(hero_image, 5, window_height - 100, 100, 100, 10)

run = True

finish = False

clock = time.Clock()


def create_asteroits():
    pass


while run:

    for e in event.get():

        if e.type == QUIT:
            run = False

        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            fire_sound.play()

            ship.fire()


    if finish != True:

        window.blit(background, (0, 0))



        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)

        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            destroyed_ships += 1
            create_monster()

        if destroyed_ships >= 200:
            finish = True
            window.blit(win, (250,250))
            window.blit(reload, (280, 280))

        if lost == 10 or hp == 0:
            finish = True
            window.blit(lose, (250, 250))
            window.blit(reload, 280, 280)


        if sprite.spritecollide(ship, monsters, dokill=True):
            hp -= 1
            if hp != 0:
                index_color -= 1
            create_monster()

        if sprite.spritecollide(ship, asteroids, dokill=True):
            hp -= 1
            if hp != 0:
             index_color -= 1
        create_asteroits()


        display.update()


    clock.tick(FPS)

quit()

