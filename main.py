# 飞机大战
import pygame
import os
from plane import MyPlane

# 游戏初始化
pygame.init()

# 屏幕大小，标题
bg_size = (480, 700)
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')

# 背景
IMG_PAHT = os.path.join(os.path.dirname(__file__), 'images')
bg_img = pygame.image.load(os.path.join(IMG_PAHT, 'background.png'))

# 分数
score = 0
myFont = pygame.font.SysFont('微软雅黑', 25)
score_img = myFont.render(str(score), True, (0, 0, 0))

myplaneGroup = pygame.sprite.Group()
myplane = MyPlane()
myplaneGroup.add(myplane)


def main():
    runner = True
    index = 0


    while runner:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False

        screen.blit(bg_img, (0, 0))
        screen.blit(score_img, (20, 10))

        myplaneGroup.update(index)
        myplaneGroup.draw(screen)
        pygame.display.update()
        index += 1
if __name__ == '__main__':
    main()
