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
        self.image=pygame.image.load(os.path.join(IMG_PAHT, 'me1.png')).convert_alpha()
        self.images = [pygame.image.load(os.path.join(IMG_PAHT, 'me{}.png'.format(i))).convert_alpha() for i in
                       range(1, 3)]
        self.rect = self.images[0].get_rect()

        self.rect.top = 550
        self.rect.left = 235


    def update(self, *arge):
        self.image = self.images[arge[0] % len(self.images)]
