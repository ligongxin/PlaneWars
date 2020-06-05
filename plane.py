# _*_encoding=utf-8_*_
# 作者     :bozhong
# 创建时间 :2020/6/513:54
# 文件     :
# IDE      :PyCharm

import pygame, os
import random

IMG_PAHT = os.path.join(os.path.dirname(__file__), 'images')


class MyPlane(pygame.sprite.Sprite):
    def __init__(self):
        super(MyPlane, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load(os.path.join(IMG_PAHT, 'me1.png')).convert_alpha(),
                                                  (60, 60))
        self.images = [pygame.transform.smoothscale(
            pygame.image.load(os.path.join(IMG_PAHT, 'me{}.png'.format(i))).convert_alpha(), (70, 70)) for i in
            range(1, 3)]
        self.destroyImages = [pygame.transform.smoothscale(
            pygame.image.load(os.path.join(IMG_PAHT, 'me_destroy_{}.png'.format(i))).convert_alpha(), (70, 70)) for i in
            range(1, 5)]
        self.rect = self.images[0].get_rect()

        self.rect.top = 550
        self.rect.left = 235
        self.isAlive = True
        self.destroytime = 0
        self.issuppluBullet = False

    def update(self, *args):
        if not self.isAlive:
            if self.destroytime < 12:
                self.image = self.destroyImages[self.destroytime // 3]
                self.destroytime += 1
            elif self.destroytime > 14:
                self.kill()
            else:
                self.destroytime += 1
        else:
            self.image = self.images[args[0] % len(self.images)]
        # self.image = self.destroyImages[args[0] % len(self.destroyImages)]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, myplane_rect):
        super(Bullet, self).__init__()
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bullet1.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top = myplane_rect.top - 10
        self.rect.left = myplane_rect.left + 33
        self.speed = 3

    def update(self, *args):
        if self.rect.top < 0:
            self.kill()
        else:
            self.rect.top -= self.speed

class SupperBulletLeft(Bullet):
    def __init__(self, myplane_rect):
        super(SupperBulletLeft, self).__init__(myplane_rect)
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bullet2.png')).convert_alpha()
        self.rect.top = myplane_rect.top
        self.rect.left = myplane_rect.left + 11
        self.speed = 5

class SupperBulletRight(Bullet):
    def __init__(self, myplane_rect):
        super(SupperBulletRight, self).__init__(myplane_rect)
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bullet2.png')).convert_alpha()
        self.rect.top = myplane_rect.top
        self.rect.left = myplane_rect.left + 51
        self.speed = 5


class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super(EnemyPlane, self).__init__()
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'enemy1.png')).convert_alpha()
        self.downImages = [pygame.image.load(os.path.join(IMG_PAHT, 'enemy1_down{}.png'.format(i))).convert_alpha() for
                           i in range(1, 5)]
        self.rect = self.image.get_rect()
        self.speed = 2
        self.rect.left = random.randrange(10, bg_size[0] - 10)
        self.height = bg_size[1]
        self.isAlive = True
        self.downtime = 0

    def update(self, *args):
        if not self.isAlive:
            if self.downtime < 8:
                self.image = self.downImages[self.downtime // 2]
                self.downtime += 1
            elif self.downtime > 12:
                self.kill()
            else:
                self.downtime += 1
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.kill()


# 补给
class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super(BulletSupply, self).__init__()
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bullet_supply.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(10, bg_size[0] - 10)
        self.height = bg_size[1]
        self.speed = 2

    def update(self, *args):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.kill()


class BombSupply(BulletSupply):
    def __init__(self, bg_size):
        super(BombSupply, self).__init__(bg_size)
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bomb_supply.png')).convert_alpha()
