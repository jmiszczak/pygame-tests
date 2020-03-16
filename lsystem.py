#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pygame as pg
import random as rnd

pg.init()

dim = 1000
screen_size = (dim, dim) 
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Trees with PyGame")
finish = False


def draw_lsystem_tree(screen, pos_start, length, ang, depth):
    if depth:
        ang_update = np.pi/8
        #color = (0, 255, 0)
        color = (rnd.randint(1,255), rnd.randint(1,255), rnd.randint(1,255))
        
        rm = np.array([[np.cos(ang), -1*np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        print(rm)
        pos_end = list(rm.dot([length, length]))

        new_end = list(np.array(pos_start)+np.array(pos_end))
        pg.draw.line(screen, color, pos_start, new_end, 2)
        
        draw_lsystem_tree(screen, new_end, length/1.2, ang+ang_update, depth-1)
        draw_lsystem_tree(screen, new_end, length/1.2, ang-ang_update, depth-1)

while not finish:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finish = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                pg.display.toggle_fullscreen()
            elif event.key == pg.K_q:
                # quit after pressing Q
                finish = True
            elif event.key == pg.K_t:
                draw_lsystem_tree(screen, (0, 0), 150, 0, 7)
            elif event.key == pg.K_c:
                # clear the screen
                screen.fill((0,0,0))
                pg.display.update()
         
    pg.display.update()

sys.exit()
