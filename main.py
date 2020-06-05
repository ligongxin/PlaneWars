# 飞机大战
import pygame
import os
from plane import MyPlane,Bullet

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

bulletGroup=pygame.sprite.Group()
clock=pygame.time.Clock()
FPS=30

def main():
    runner = True
    index = 0


    while runner:
        clock.tick(FPS)

        if index % 20 ==0:
            for myplane in myplaneGroup:
                    bullet=Bullet(myplane.rect)
                    bulletGroup.add(bullet)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False

        mykeyslist = pygame.key.get_pressed()
        if mykeyslist[pygame.K_RIGHT]:
            for myplane in myplaneGroup:
                if myplane.rect.right < bg_size[0]:
                    myplane.rect.left += 5
        elif mykeyslist[pygame.K_LEFT]:
            for myplane in myplaneGroup:
                if myplane.rect.left > 0 :
                    myplane.rect.left -= 5
        elif mykeyslist[pygame.K_UP]:
            for myplane in myplaneGroup:
                if myplane.rect.top > 0 :
                    myplane.rect.top -= 5
        elif mykeyslist[pygame.K_DOWN]:
            for myplane in myplaneGroup:
                if myplane.rect.bottom < bg_size[1] :
                    myplane.rect.bottom += 5

        screen.blit(bg_img, (0, 0))
        screen.blit(score_img, (20, 10))

        myplaneGroup.update(index)
        myplaneGroup.draw(screen)
        bulletGroup.update(index)
        bulletGroup.draw(screen)
        pygame.display.update()
        index += 1
if __name__ == '__main__':
    main()
