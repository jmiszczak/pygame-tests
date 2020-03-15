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

size = (400,350) 
screen = pg.display.set_mode((400,350))
pg.display.set_caption("Some tests with PyGame")
finish = False

while not finish:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finish = True
                      
    color = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
    position = (rnd.randint(1,size[0]), rnd.randint(1, size[1]))
    pg.draw.circle(screen, color, position, 5)
    pg.display.update()

sys.exit()
