#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:26:15 2020

@author: jam
"""
#%%
import sys
import numpy as np
import numpy.random as rnd

import pygame as pg

#%%
pg.init()

dim = 1000
screen_size = (dim, dim) 
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Fractals with PyGame")
finish = False

def draw_sierpinski_triangel(screen, position, length, depth):
    if depth:
        color = (rnd.randint(0,255),rnd.randint(0,255),rnd.randint(0,255))
        pg.draw.lines(screen, color, True, 
                [
                    position, 
                    (position[0]+length, position[1]), 
                    (position[0]+length/2, position[1]+np.sqrt(3)*length/2)
                    ]
                )
        draw_sierpinski_triangel(screen, position, length/2, depth-1)
        draw_sierpinski_triangel(screen, (position[0]+length/2, position[1]), length/2, depth-1)
        draw_sierpinski_triangel(screen, (position[0]+length/4, position[1]+np.sqrt(3)*length/4), length/2, depth-1)


def draw_sierpinski_square(screen, position, length, depth):
    if depth: 
        color = (rnd.randint(0,255),rnd.randint(0,255),rnd.randint(0,255))
        rect = (position, (length, length))
        pg.draw.rect(screen, color, rect, 1)
        draw_sierpinski_square(screen, position, length/3, depth-1)
        draw_sierpinski_square(screen, (position[0]+length/3, position[1]), length/3, depth-1)
        draw_sierpinski_square(screen, (position[0]+2*length/3, position[1]), length/3, depth-1)
        draw_sierpinski_square(screen, (position[0], position[1]+length/3), length/3, depth-1)
        draw_sierpinski_square(screen, (position[0], position[1]+2*length/3), length/3, depth-1)
        draw_sierpinski_square(screen, (position[0]+length/3, position[1]+2*length/3), length/3, depth-1)
        draw_sierpinski_square(screen, (position[0]+2*length/3, position[1]+length/3), length/3, depth-1)
        draw_sierpinski_square(screen, (position[0]+2*length/3, position[1]+2*length/3), length/3, depth-1)


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
            elif event.key == pg.K_s:
                draw_sierpinski_square(screen, (0,0), dim, 5)
            elif event.key == pg.K_t:
                draw_sierpinski_triangel(screen, (0,0), dim, 6)
            elif event.key == pg.K_c:
                # clear the screen
                screen.fill((0,0,0))
                pg.display.update()
         
#    color = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
#    position = (rnd.randint(1,screen_size[0]), rnd.randint(1, screen_size[1]))
#    pg.draw.circle(screen, color, position, 5)
    pg.display.update()

sys.exit()
