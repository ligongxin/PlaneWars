# 飞机大战
import pygame
import os, random, time
from plane import MyPlane, Bullet, EnemyPlane, BulletSupply, BombSupply, SupperBulletLeft, SupperBulletRight
from plane import Bomb, EnemyMiddle, BigEnemy

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
# myFont = pygame.font.SysFont('微软雅黑', 25)
# score_img = myFont.render(str(score), True, (0, 0, 0))


# 子弹精灵组
bulletGroup = pygame.sprite.Group()

# 敌机精灵组
enemyGroup = pygame.sprite.Group()

# 补给精灵组
supplyGroup = pygame.sprite.Group()

clock = pygame.time.Clock()
FPS = 60

GUN_BULLET_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GUN_BULLET_EVENT, 100)

# 暂停按钮
pause_nor_img = pygame.image.load(os.path.join(IMG_PAHT, 'pause_nor.png'))
pause_pressed_img = pygame.image.load(os.path.join(IMG_PAHT, 'pause_pressed.png'))
# 开始、jixu
resume_nor_img = pygame.image.load(os.path.join(IMG_PAHT, 'resume_nor.png'))
resume_pressed_img = pygame.image.load(os.path.join(IMG_PAHT, 'resume_pressed.png'))

# 生命小飞机
plane_life_img = pygame.image.load(os.path.join(IMG_PAHT, 'life.png'))

RED = (225, 0, 0)
GREEN = (0, 225, 0)


def main():
    global score, score_img

    # 我方战机
    myplaneGroup = pygame.sprite.Group()
    myplane = MyPlane()
    myplaneGroup.add(myplane)

    runner = True
    index = 1

    # 全屏炸弹
    bomb = Bomb()

    # 全屏炸弹数量
    bomb_num = 3

    # 暂停按钮
    pause_flag = True
    resume_flag = True

    # 生命条数：
    plane_life = 2
    while runner:
        clock.tick(FPS)
        if index > 10000:
            index = 0

        if index % 60 == 0:
            enemyplane = EnemyPlane(bg_size)
            enemyGroup.add(enemyplane)
        if index % 120 == 0:
            enemyplane = EnemyMiddle(bg_size)
            enemyGroup.add(enemyplane)
        if index % 200 == 0:
            bigenemy = BigEnemy(bg_size)
            enemyGroup.add((bigenemy))
            # if index %1 ==0:
            #     bigenemy.health_bar(screen,RED)

        if index % 500 == 0:
            Supply = random.choice([BulletSupply(bg_size), BombSupply(bg_size)])
            # Supply=BombSupply(bg_size)
            supplyGroup.add(Supply)
        screen.blit(bg_img, (0, 0))
        if len(myplaneGroup) == 0:
            # 重新生成我方飞机
            if plane_life > 0:
                myplaneGroup = pygame.sprite.Group()
                myplane = MyPlane()
                myplaneGroup.add(myplane)
                plane_life -= 1
            else:
                print('game over')
                runner = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if 0 < bomb_num <= 3:
                        bomb_num -= 1
                        for enemyplane in enemyGroup:
                            if enemyplane.rect.top > 0:
                                # enemyplane.isAlive = False
                                enemyplane.energy = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if bg_size[0] - 55 < x < bg_size[0] and 0 < y < bg_size[1] - 655:
                    if event.button == 1:
                        resume_flag = not resume_flag

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if bg_size[0] - 55 < x < bg_size[0] and 0 < y < bg_size[1] - 655:
                    if event.button == 1:
                        pause_flag = not pause_flag
                        resume_flag = not resume_flag

            if event.type == GUN_BULLET_EVENT:
                for myplane in myplaneGroup:

                    if time.time() - myplane.supplyBullettime < 10:
                        bullet_1 = SupperBulletLeft(myplane.rect)
                        bullet_2 = SupperBulletRight(myplane.rect)
                        bulletGroup.add(bullet_1, bullet_2)
                    # if time.time() -myplane.supplyBombtime<10:
                    #     bomb=Bomb(myplane.rect)
                    #     bulletGroup.add(bomb)
                    # else:
                    bullet = Bullet(myplane.rect)
                    bulletGroup.add(bullet)

        mykeyslist = pygame.key.get_pressed()
        if mykeyslist[pygame.K_RIGHT]:
            for myplane in myplaneGroup:
                if myplane.rect.right < bg_size[0]:
                    myplane.rect.left += 5
        elif mykeyslist[pygame.K_LEFT]:
            for myplane in myplaneGroup:
                if myplane.rect.left > 0:
                    myplane.rect.left -= 5
        elif mykeyslist[pygame.K_UP]:
            for myplane in myplaneGroup:
                if myplane.rect.top > 0:
                    myplane.rect.top -= 5
        elif mykeyslist[pygame.K_DOWN]:
            for myplane in myplaneGroup:
                if myplane.rect.bottom < bg_size[1] - 60:
                    myplane.rect.bottom += 5
        # 子弹与敌机碰撞,分数增加
        for bullet in bulletGroup:
            for enemyplane in enemyGroup:
                if type(enemyplane) == EnemyPlane:
                    if pygame.sprite.collide_mask(bullet, enemyplane):
                        bulletGroup.remove(bullet)
                        enemyplane.isAlive = False
                        enemyplane.energy -= 1
                        # if enemyplane.isAlive ==False:
                        #     print(enemyplane.isAlive)
                        if enemyplane.energy == 0:
                            score += 10

                elif type(enemyplane) == EnemyMiddle:
                    if pygame.sprite.collide_mask(bullet, enemyplane):
                        bulletGroup.remove(bullet)
                        enemyplane.energy -= 1
                        # enemyplane.isAlive = False
                        if enemyplane.energy == 0:
                            score += 100

                else:
                    if pygame.sprite.collide_mask(bullet, enemyplane):
                        bulletGroup.remove(bullet)
                        enemyplane.energy -= 1
                        # enemyplane.isAlive = False
                        if enemyplane.energy == 0:
                            score += 1000

        # 我方战机与敌机碰撞
        for myplane in myplaneGroup:
            for enemyplane in enemyGroup:
                if pygame.sprite.collide_mask(myplane, enemyplane):
                    if myplane.invincible or time.time() - myplane.createtime < 3:
                        enemyplane.isAlive = False
                    else:
                        enemyplane.isAlive = False
                        myplane.isAlive = False

        # 我方战机与补给碰撞
        for myplane in myplaneGroup:
            for supply in supplyGroup:
                # if isinstance(supply,BulletSupply):
                if type(supply) == BulletSupply:
                    if pygame.sprite.collide_mask(myplane, supply):
                        supplyGroup.remove(supply)
                        # myplane.issupplyBullet =True
                        myplane.supplyBullettime = time.time()
                else:
                    if pygame.sprite.collide_mask(myplane, supply):
                        supplyGroup.remove(supply)
                        if bomb_num < 3:
                            bomb_num += 1
                        else:
                            bomb_num = 3

        # 补给，全屏炸弹

        #     bulletGroup.add(bomb)
        myFont = pygame.font.SysFont('微软雅黑', 35)
        score_img = myFont.render('sorce: {}'.format(score), True, (0, 0, 0))

        screen.blit(score_img, (20, 10))
        # 绘制全屏炸弹和数量
        screen.blit(bomb.image, (bomb.rect))

        # 绘制分数
        myFont = pygame.font.SysFont('微软雅黑', 40)
        bomb_num_img = myFont.render(' x  {}'.format(bomb_num), True, (0, 0, 0))
        screen.blit(bomb_num_img, (bomb.rect.left + 70, bomb.rect.top + 16))

        # 绘制暂停按钮
        if pause_flag:
            if resume_flag:
                screen.blit(pause_nor_img, (bg_size[0] - 55, bg_size[1] - 695))
            else:
                screen.blit(pause_pressed_img, (bg_size[0] - 55, bg_size[1] - 695))
        else:
            if resume_flag:
                screen.blit(resume_nor_img, (bg_size[0] - 55, bg_size[1] - 695))
            else:
                screen.blit(resume_pressed_img, (bg_size[0] - 55, bg_size[1] - 695))

        # 生命小飞机绘制
        if plane_life == 2:
            for i in [(370, 640), (420, 640)]:
                screen.blit(plane_life_img, i)
        elif plane_life == 1:
            screen.blit(plane_life_img, (420, 640))

        # pygame.draw.rect(screen, RED, [2, 15, 400, 10], 0)
        # pygame.draw.rect(screen, GREEN, [2, 15, 380, 10], 0)
        index += 1
        myplaneGroup.update(index)
        myplaneGroup.draw(screen)
        bulletGroup.update(index)
        bulletGroup.draw(screen)
        enemyGroup.update(index, screen, RED, GREEN)
        enemyGroup.draw(screen)
        supplyGroup.update(index)
        supplyGroup.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
    # res=random.choice(['j','k'])
    # print(res)
