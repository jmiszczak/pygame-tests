#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:26:15 2020

@author: jam
"""
#%%
import pygame as pg
import random as rnd
import sys

#%%
pg.init()

#screen_size = (2560,1440) 
screen_size = (1920, 1080)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Some tests with PyGame")
finish = False

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
                      
    color = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
    position = (rnd.randint(1,screen_size[0]), rnd.randint(1, screen_size[1]))
    pg.draw.circle(screen, color, position, 10)
    pg.display.update()

sys.exit()
