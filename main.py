# 飞机大战
import pygame
import os,random,time
from plane import MyPlane, Bullet,EnemyPlane,BulletSupply,BombSupply,SupperBulletLeft,SupperBulletRight
from plane import Bomb,EnemyMiddle
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

# 我方战机
myplaneGroup = pygame.sprite.Group()
myplane = MyPlane()
myplaneGroup.add(myplane)

# 子弹精灵组
bulletGroup = pygame.sprite.Group()

# 敌机精灵组
enemyGroup = pygame.sprite.Group()

#补给精灵组
supplyGroup=pygame.sprite.Group()

clock = pygame.time.Clock()
FPS = 60

GUN_BULLET_EVENT=pygame.USEREVENT +1
pygame.time.set_timer(GUN_BULLET_EVENT,200)
def main():
    global score,score_img
    runner = True
    index = 0

    while runner:
        clock.tick(FPS)

        if index %60 ==0:
            enemyplane=EnemyPlane(bg_size)
            enemyGroup.add(enemyplane)
        if index %120 ==0:
            enemyplane = EnemyMiddle(bg_size)
            enemyGroup.add(enemyplane)
        if index % 500 ==0:
            Supply=random.choice([BulletSupply(bg_size),BombSupply(bg_size)])
            # Supply=BombSupply(bg_size)
            supplyGroup.add(Supply)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False

            if event.type == GUN_BULLET_EVENT:
                for myplane in myplaneGroup:

                    if time.time() -myplane.supplyBullettime<10:
                        bullet_1=SupperBulletLeft(myplane.rect)
                        bullet_2= SupperBulletRight(myplane.rect)
                        bulletGroup.add(bullet_1,bullet_2)
                    if time.time() -myplane.supplyBombtime<10:
                        bomb=Bomb(myplane.rect)
                        bulletGroup.add(bomb)
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
                if myplane.rect.bottom < bg_size[1]:
                    myplane.rect.bottom += 5
        #子弹与敌机碰撞,分数增加
        for bullet in bulletGroup:
            for enemyplane in enemyGroup:
                if type(enemyplane)==EnemyPlane:
                    if pygame.sprite.collide_mask(bullet,enemyplane):
                        bulletGroup.remove(bullet)
                        enemyplane.isAlive = False
                    # if enemyplane.isAlive ==False:
                    #     print(enemyplane.isAlive)
                        score +=1
                        myFont = pygame.font.SysFont('微软雅黑', 25)
                        score_img = myFont.render(str(score), True, (0, 0, 0))
                elif type(enemyplane)==EnemyMiddle:
                    if pygame.sprite.collide_mask(bullet, enemyplane):
                        bulletGroup.remove(bullet)
                        enemyplane.energy -=1


        #我方战机与敌机碰撞
        for myplane in myplaneGroup:
            for enemyplane in enemyGroup:
                if pygame.sprite.collide_mask(myplane, enemyplane):
                    enemyplane.isAlive = False
                    myplane.isAlive =False

        # 我方战机与补给碰撞
        for myplane in myplaneGroup:
            for supply in supplyGroup:
                # if isinstance(supply,BulletSupply):
                if type(supply) ==BulletSupply:
                    if pygame.sprite.collide_mask(myplane,supply):
                        supplyGroup.remove(supply)
                        # myplane.issupplyBullet =True
                        myplane.supplyBullettime=time.time()
                else:
                    if pygame.sprite.collide_mask(myplane, supply):
                        supplyGroup.remove(supply)
                        # myplane.supplyBombtime = time.time()

        if len(myplaneGroup) ==0:
            runner=False

        screen.blit(bg_img, (0, 0))
        screen.blit(score_img, (20, 10))

        index += 1
        myplaneGroup.update(index)
        myplaneGroup.draw(screen)
        bulletGroup.update(index)
        bulletGroup.draw(screen)
        enemyGroup.update(index)
        enemyGroup.draw(screen)
        supplyGroup.update(index)
        supplyGroup.draw(screen)

        pygame.display.update()



if __name__ == '__main__':
    main()
    # res=random.choice(['j','k'])
    # print(res)