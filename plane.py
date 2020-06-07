# _*_encoding=utf-8_*_
# 作者     :bozhong
# 创建时间 :2020/6/513:54
# 文件     :
# IDE      :PyCharm

import pygame, os
import random, time

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
        self.supplyBullettime = 0
        self.invincible = False
        self.createtime = time.time()

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
        self.speed = 10

    def update(self, *args):
        if self.rect.top < 0:
            self.kill()
        else:
            self.rect.top -= self.speed


class Bomb():
    def __init__(self, ):
        # super(Bomb, self).__init__()
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bomb.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top = 630
        self.rect.left = 10
        # self.speed = 10


class SupperBulletLeft(Bullet):
    def __init__(self, myplane_rect):
        super(SupperBulletLeft, self).__init__(myplane_rect)
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bullet2.png')).convert_alpha()
        self.rect.top = myplane_rect.top
        self.rect.left = myplane_rect.left + 11
        self.speed = 10


class SupperBulletRight(Bullet):
    def __init__(self, myplane_rect):
        super(SupperBulletRight, self).__init__(myplane_rect)
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bullet2.png')).convert_alpha()
        self.rect.top = myplane_rect.top
        self.rect.left = myplane_rect.left + 58
        self.speed = 10


class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super(EnemyPlane, self).__init__()
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'enemy1.png')).convert_alpha()
        self.downImages = [pygame.image.load(os.path.join(IMG_PAHT, 'enemy1_down{}.png'.format(i))).convert_alpha() for
                           i in range(1, 5)]
        self.rect = self.image.get_rect()
        self.speed = 4
        self.rect.left = random.randrange(57, bg_size[0] - 57)
        self.height = bg_size[1]
        self.width = bg_size[0]
        self.isAlive = True
        self.downtime = 0
        self.energy = 1

    def update(self, *args):
        # if not self.isAlive:
        if self.energy <= 0:
            if self.downtime < 8:
                self.image = self.downImages[self.downtime // 2]
                self.downtime += 1
            elif self.downtime > 9:
                self.kill()
            else:
                self.downtime += 1
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.rect.bottom = 0

    # 敌机生命条
    def health_bar(self, screen, color, width=160):
        pygame.draw.rect(screen, color, [self.rect.left, self.rect.top - 5, width, 2], 0)


# 补给
class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super(BulletSupply, self).__init__()
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'bullet_supply.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(60, bg_size[0] - 60)
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


class EnemyMiddle(EnemyPlane):
    def __init__(self, bg_size):
        super(EnemyMiddle, self).__init__(bg_size)
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'enemy2.png')).convert_alpha()
        self.downImages = [pygame.image.load(os.path.join(IMG_PAHT, 'enemy2_down{}.png'.format(i))).convert_alpha() for
                           i in range(1, 5)]
        self.rect.left = random.randrange(69, bg_size[0] - 69)
        self.energy = 5
        self.speed = 2
        self.rect.bottom = -30

    def update(self, *args):

        # if not self.isAlive:
        if self.energy <= 0:
            self.energy = 0
            if self.downtime < 8:
                self.image = self.downImages[self.downtime // 2]
                self.downtime += 1
            elif self.downtime > 12:
                self.kill()
            else:
                self.downtime += 1
        if self.rect.top < self.height:
            self.rect.top += self.speed
            if self.width // 4 < self.rect.left < self.width:
                self.rect.left -= 1
            elif 0 < self.rect.left <= self.width // 4:
                self.rect.left += 1
            else:
                self.rect.bottom = -30
            self.health_bar(args[1], args[2], width=70)
            self.health_bar(args[1], args[3], width=self.energy * 14)


class BigEnemy(EnemyPlane):
    def __init__(self, bg_size):
        super(BigEnemy, self).__init__(bg_size)
        self.image = pygame.image.load(os.path.join(IMG_PAHT, 'enemy3_hit.png')).convert_alpha()
        self.images = [pygame.image.load(os.path.join(IMG_PAHT, 'enemy3_n{}.png'.format(i))).convert_alpha() for i in
                       range(1, 3)]
        self.downImages = [pygame.image.load(os.path.join(IMG_PAHT, 'enemy3_down{}.png'.format(i))).convert_alpha() for
                           i in range(1, 7)]

        self.energy = 32
        # self.rect.left = random.randrange(bg_size[0] - 100)
        self.rect.left = random.randrange(169, bg_size[0] - 169)
        self.rect.bottom = -150
        self.speed = 1

    def update(self, *args):
        # if not self.isAlive:
        if self.energy <= 0:
            self.energy = 0
            if self.downtime < 12:
                self.image = self.downImages[self.downtime // 2]
                self.downtime += 1
            elif self.downtime > 14:
                self.kill()
            else:
                self.downtime += 1
        if self.rect.top < self.height:
            self.rect.top += self.speed
            if self.energy > 0:
                self.image = self.images[args[0] % len(self.images)]
                # if self.width//4 <self.rect.left <self.width:
                #     self.rect.left -=1
                # elif 0<self.rect.left <=self.width//4:
                #     self.rect.left += 1
        else:
            self.rect.bottom = -150
        self.health_bar(args[1], args[2])
        self.health_bar(args[1], args[3], width=self.energy * 5)

    # 敌机生命条
    def health_bar(self, screen, color, width=160):
        pygame.draw.rect(screen, color, [self.rect.left, self.rect.top - 5, width, 2], 0)
