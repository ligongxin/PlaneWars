# _*_encoding=utf-8_*_
# 作者     :bozhong
# 创建时间 :2020/6/513:54
# 文件     :
# IDE      :PyCharm

import pygame, os

IMG_PAHT = os.path.join(os.path.dirname(__file__), 'images')


class MyPlane(pygame.sprite.Sprite):
    def __init__(self):
        super(MyPlane, self).__init__()
        self.image=pygame.transform.smoothscale(pygame.image.load(os.path.join(IMG_PAHT, 'me1.png')).convert_alpha(),(60,60))
        self.images = [pygame.transform.smoothscale(pygame.image.load(os.path.join(IMG_PAHT, 'me{}.png'.format(i))).convert_alpha(),(60,60)) for i in
                       range(1, 3)]
        self.rect = self.images[0].get_rect()

        self.rect.top = 550
        self.rect.left = 235


    def update(self, *args):
        self.image = self.images[args[0] % len(self.images)]


class Bullet(pygame.sprite.Sprite):
    def __init__(self,myplane_rect):
        super(Bullet,self).__init__()
        self.image=pygame.image.load(os.path.join(IMG_PAHT, 'bullet1.png')).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.top=myplane_rect.top-10
        self.rect.left = myplane_rect.left+29
        self.speed=1

    def update(self, *args):
        if self.rect.top <0:
            self.kill()
        else:
            self.rect.top -= self.speed