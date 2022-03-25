import os
import time

import pygame as pg


def main():
    exit_flag = False
    FPS = 60
    pg.init()

    pg.display.set_caption("fake_news")
    surface = pg.display.set_mode((800, 600))
    icon = pg.image.load(
        'cursor.png').convert_alpha()
    pg.display.set_icon(icon)
    # 加载本地图片
    bgSurface = pg.image.load(
        'BG.jpg').convert()
    bgSurface = pg.transform.scale(bgSurface, (800, 600))
    # 获取游戏时钟
    clock = pg.time.Clock()
    # 图片缩放
    scaleImg = pg.transform.scale(icon, (40, 30))
    # 获取图片的矩形框
    rect = scaleImg.get_rect()
    # 移动步长
    step = 10
    # 绘制背景
    surface.blit(bgSurface, (0, 0))
    # 刷新帧率
    newRect = None
    while not exit_flag:
        clock.tick(FPS)
        # 重新绘制背景指定区域，等同于擦除图片效果
        if rect:
            surface.blit(bgSurface, rect, rect)
        # 图片移动指定步长
        newRect = rect.move(step, 0)
        # 弹出事件，这个一定要写，要不事件栈满了之后就会卡死
        for event in pg.event.get():
            # 点击关闭
            if event.type == pg.QUIT:
                exit_flag = True
        # 绘制图片到屏幕画布指定区域
        surface.blit(scaleImg, newRect)
        # 控制在窗口内来回移动
        if newRect.x > 800 - newRect.w:
            step = -10
        elif newRect.x < 0:
            step = 10

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        # 更新绘制到屏幕上
        pg.display.update([rect, newRect])
        rect = newRect



if __name__ == '__main__':
    main()
