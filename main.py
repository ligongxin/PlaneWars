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
# 音乐主路径
MUSIC_PATH = os.path.join(os.path.dirname(__file__), 'music')
# 初始化音乐
pygame.mixer.init()

pygame.mixer.music.load(os.path.join(MUSIC_PATH, 'game_music.ogg'))
bullet_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'bullet.wav'))
botton_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'button.wav'))
small_enemydown_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'enemy1_down.wav'))
middle_enemydown_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'enemy2_down.wav'))
big_enemydown_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'enemy3_down.wav'))
big_enemyfly_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'enemy3_flying.wav'))
get_bomb_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'get_bomb.wav'))
get_bullet_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'get_bullet.wav'))
me_down_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'me_down.wav'))
supply_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'supply.wav'))
use_bomb_music = pygame.mixer.Sound(os.path.join(MUSIC_PATH, 'use_bomb.wav'))

# 暂停按钮
pause_nor_img = pygame.image.load(os.path.join(IMG_PAHT, 'pause_nor.png'))
pause_pressed_img = pygame.image.load(os.path.join(IMG_PAHT, 'pause_pressed.png'))
# 开始、jixu
resume_nor_img = pygame.image.load(os.path.join(IMG_PAHT, 'resume_nor.png'))
resume_pressed_img = pygame.image.load(os.path.join(IMG_PAHT, 'resume_pressed.png'))

# 生命小飞机
plane_life_img = pygame.image.load(os.path.join(IMG_PAHT, 'life.png'))
life_rect = plane_life_img.get_rect()

# 重新开始，结束游戏
again_img = pygame.image.load(os.path.join(IMG_PAHT, 'again.png'))
gameover_img = pygame.image.load(os.path.join(IMG_PAHT, 'gameover.png'))

RED = (225, 0, 0)
GREEN = (0, 225, 0)
WRITE = (225, 225, 225)

# 子弹精灵组
bulletGroup = pygame.sprite.Group()

# 敌机精灵组
enemyGroup = pygame.sprite.Group()

# 补给精灵组
supplyGroup = pygame.sprite.Group()

clock = pygame.time.Clock()
FPS = 60

# 子弹定时器
GUN_BULLET_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GUN_BULLET_EVENT, 200)


def main():
    # 分数
    score = 0
    runner = True
    index = 1

    # 我方战机
    myplaneGroup = pygame.sprite.Group()
    myplane = MyPlane()
    myplaneGroup.add(myplane)

    # 全屏炸弹
    bomb = Bomb()

    # 全屏炸弹数量
    bomb_num = 3

    # 暂停按钮
    pause_flag = True
    resume_flag = True

    # 生命条数：
    plane_life_num = 3

    # 读取文档的标准
    read_flag = True
    # 播放背景音
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # 关卡难度
    level = 1
    # 敌机生成速度
    sm_em = 120
    mi_em = 900
    bi_em = 200
    # 补给生成速度
    sup_speed = 900
    # 子弹速度
    bullet_spend = 10
    while runner:
        clock.tick(FPS)
        # 关卡难度
        if level == 1:
            if score > 200:
                level += 1
            sm_em = 100
        elif level == 2:
            if score > 1000:
                level += 1
            sm_em = 80
            mi_em = 700
        elif level == 3:
            if score > 2000:
                level += 1
            sm_em = 60
            mi_em = 500
            bi_em = 1800
            bullet_spend = 8
        elif level == 4:
            if score > 4000:
                level += 1
            sm_em = 40
            mi_em = 300
            bi_em = 1200
            bullet_spend = 6
        elif level == 5:
            if score > 4000:
                level += 1
            sm_em = 20
            mi_em = 300
            bi_em = 1000
            bullet_spend = 5
        # 我方生命数量大于0
        if plane_life_num > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runner = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if bg_size[0] - 55 < x < bg_size[0] and 0 < y < bg_size[1] - 655:
                        if event.button == 1:
                            botton_music.play()
                            resume_flag = not resume_flag

                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if bg_size[0] - 55 < x < bg_size[0] and 0 < y < bg_size[1] - 655:
                        if event.button == 1:
                            botton_music.play()
                            pause_flag = not pause_flag
                            resume_flag = not resume_flag
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if pause_flag:
                            if 0 < bomb_num <= 3:
                                bomb_num -= 1
                                use_bomb_music.play()
                                for enemyplane in enemyGroup:
                                    if enemyplane.rect.top > 0:
                                        # enemyplane.isAlive = False
                                        enemyplane.energy = 0

                # if event.type == GUN_BULLET_EVENT:
                #     for myplane in myplaneGroup:
                #         if pause_flag:
                #             if time.time() - myplane.supplyBullettime < 10:
                #                 bullet_1 = SupperBulletLeft(myplane.rect)
                #                 bullet_2 = SupperBulletRight(myplane.rect)
                #                 bulletGroup.add(bullet_1, bullet_2)
                #             bullet_music.set_volume(0.4)
                #             bullet_music.play()
                #             bullet = Bullet(myplane.rect)
                #             bulletGroup.add(bullet)

            # 绘制屏幕
            screen.blit(bg_img, (0, 0))
            # 是否已按暂停
            if pause_flag:
                if index > 10000:
                    index = 0
                # 生成敌机--小
                if index % sm_em == 0:
                    enemyplane = EnemyPlane(bg_size)
                    enemyGroup.add(enemyplane)
                # 生成敌机--中
                if index % mi_em == 0:
                    enemyplane = EnemyMiddle(bg_size)
                    enemyGroup.add(enemyplane)
                # 生成敌机--大
                if index % bi_em == 0:
                    bigenemy = BigEnemy(bg_size)
                    enemyGroup.add((bigenemy))
                    big_enemyfly_music.play(-1)
                    # if index %1 ==0:
                    #     bigenemy.health_bar(screen,RED)
                # 随机生成补给
                if index % sup_speed == 0:
                    Supply = random.choice([BulletSupply(bg_size), BombSupply(bg_size)])
                    # Supply=BombSupply(bg_size)
                    supplyGroup.add(Supply)
                    supply_music.play()

                # 生成子弹
                if index % bullet_spend == 0:
                    for myplane in myplaneGroup:
                        if time.time() - myplane.supplyBullettime < 10:
                            bullet_1 = SupperBulletLeft(myplane.rect)
                            bullet_2 = SupperBulletRight(myplane.rect)
                            bulletGroup.add(bullet_1, bullet_2)
                        bullet_music.set_volume(0.4)
                        bullet_music.play()
                        bullet = Bullet(myplane.rect)
                        bulletGroup.add(bullet)

                if len(myplaneGroup) == 0:
                    # 重新生成我方飞机
                    if plane_life_num > 0:
                        myplaneGroup = pygame.sprite.Group()
                        myplane = MyPlane()
                        myplaneGroup.add(myplane)
                        plane_life_num -= 1

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
                                    small_enemydown_music.play()
                                    score += 10

                        elif type(enemyplane) == EnemyMiddle:
                            if pygame.sprite.collide_mask(bullet, enemyplane):
                                # 音乐播放
                                # bullet_music.play()
                                bulletGroup.remove(bullet)
                                enemyplane.energy -= 1
                                # enemyplane.isAlive = False
                                if enemyplane.energy == 0:
                                    middle_enemydown_music.play()
                                    big_enemyfly_music.stop()
                                    score += 100

                        elif type(enemyplane) == BigEnemy:
                            if pygame.sprite.collide_mask(bullet, enemyplane):
                                # 音乐播放
                                # bullet_music.play()
                                bulletGroup.remove(bullet)
                                enemyplane.energy -= 1
                                # enemyplane.isAlive = False
                                if enemyplane.energy == 0:
                                    big_enemydown_music.play()
                                    score += 1000

                # 我方战机与敌机碰撞
                for myplane in myplaneGroup:
                    for enemyplane in enemyGroup:
                        if pygame.sprite.collide_mask(myplane, enemyplane):
                            if myplane.invincible or time.time() - myplane.createtime < 3:
                                enemyplane.isAlive = False
                            else:
                                me_down_music.play()
                                enemyplane.isAlive = False
                                myplane.isAlive = False

                # 我方战机与补给碰撞
                for myplane in myplaneGroup:
                    for supply in supplyGroup:
                        # if isinstance(supply,BulletSupply):
                        if type(supply) == BulletSupply:
                            if pygame.sprite.collide_mask(myplane, supply):
                                get_bullet_music.play()
                                supplyGroup.remove(supply)
                                # myplane.issupplyBullet =True
                                myplane.supplyBullettime = time.time()
                        else:
                            if pygame.sprite.collide_mask(myplane, supply):
                                get_bomb_music.play()
                                supplyGroup.remove(supply)
                                if bomb_num < 3:
                                    bomb_num += 1
                                else:
                                    bomb_num = 3

                index += 1
                myplaneGroup.update(index)
                myplaneGroup.draw(screen)
                bulletGroup.update(index)
                bulletGroup.draw(screen)
                enemyGroup.update(index, screen, RED, GREEN)
                enemyGroup.draw(screen)
                supplyGroup.update(index)
                supplyGroup.draw(screen)

            # 绘制分数
            myFont = pygame.font.SysFont('arial', 35)
            score_img = myFont.render('Score: {}'.format(score), True, WRITE)
            screen.blit(score_img, (20, 10))
            # 绘制全屏炸弹和数量
            screen.blit(bomb.image, (bomb.rect))
            # 补给，全屏炸弹
            myFont = pygame.font.SysFont('arial', 40)
            bomb_num_img = myFont.render(' x  {}'.format(bomb_num), True, (0, 0, 0))
            screen.blit(bomb_num_img, (bomb.rect.left + 70, bomb.rect.top + 16))
            # 生命小飞机绘制
            if plane_life_num:
                for i in range(plane_life_num):
                    screen.blit(plane_life_img,
                                (bg_size[0] - 10 - (i + 1) * life_rect.width, bg_size[1] - 10 - life_rect.height))


        # 当生命值为0时，结束游戏，绘制结束游戏画面
        elif plane_life_num == 0:
            clock.tick(FPS * 2)
            big_enemyfly_music.stop()
            # print('game over')
            screen.blit(bg_img, (0, 0))
            screen.blit(again_img, (bg_size[0] - 390, bg_size[1] // 1.5))
            screen.blit(gameover_img, (bg_size[0] - 390, bg_size[1] // 1.5 + 50))

            # 获取历史最高分数,为了防止每一帧都打开文件，只需要读取一次就好啦
            if read_flag:
                read_flag = not read_flag
                # 读取历史最高分
                with open('score.txt', 'r') as f:
                    bast_score = int(f.read())

                # 判断当前分数与历史分数比较
                if bast_score < score:
                    with open('score.txt', 'w') as f:
                        f.write(str(score))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runner = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_key = pygame.mouse.get_pressed()
                    if pressed_key[0] == 1:
                        x, y = pygame.mouse.get_pos()
                        # 选择重新开始，生命初始化，清除屏幕
                        if bg_size[0] - 390 < x < bg_size[0] - 90 and bg_size[1] // 1.5 < y < bg_size[1] // 1.5 + 41:
                            botton_music.play()
                            plane_life_num = 3
                            index = 1
                            score = 0
                            level = 1
                            read_flag = True
                            # 清除敌机
                            for enemyplane in enemyGroup:
                                enemyplane.kill()
                            # 清除子弹
                            for bullet in bulletGroup:
                                bullet.kill()
                            # 清除补给
                            for supply in supplyGroup:
                                supply.kill()

                        elif bg_size[0] - 390 < x < bg_size[0] - 90 and bg_size[1] // 1.5 + 50 < y < bg_size[
                            1] // 1.5 + 91:
                            botton_music.play()
                            runner = False

            myFont = pygame.font.SysFont('STKaiti', 40)
            bast_score_img = myFont.render('  Bast:  {}'.format(bast_score), True, WRITE)
            score_font = pygame.font.SysFont('楷体', 60)
            your_score_img = score_font.render('Your   Score', True, WRITE)
            score_font = pygame.font.SysFont('楷体', 80)
            score_show = score_font.render(str(score), True, WRITE)
            screen.blit(bast_score_img, (20, 10))
            screen.blit(your_score_img, (130, 240))
            screen.blit(score_show, (190, 320))

        # 绘制暂停按钮
        if pause_flag:
            # 重新打开背景音
            pygame.mixer.music.unpause()
            if resume_flag:
                screen.blit(pause_nor_img, (bg_size[0] - 55, bg_size[1] - 695))
            else:
                screen.blit(pause_pressed_img, (bg_size[0] - 55, bg_size[1] - 695))
        else:
            screen.blit(bg_img, (0, 0))
            myFont = pygame.font.SysFont('arial', 35)
            score_img = myFont.render('Score: {}'.format(score), True, (225, 225, 225))
            screen.blit(score_img, (20, 10))
            # pygame.time.set_timer(GUN_BULLET_EVENT,200)
            # 暂停背景音播放
            pygame.mixer.music.pause()
            big_enemyfly_music.stop()
            if resume_flag:
                screen.blit(resume_nor_img, (bg_size[0] - 55, bg_size[1] - 695))

            else:
                screen.blit(resume_pressed_img, (bg_size[0] - 55, bg_size[1] - 695))

        pygame.display.update()


if __name__ == '__main__':
    main()
    # res=random.choice(['j','k'])
    # print(res)
