#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:26:15 2020

@author: jam
"""
#%%
import pygame as pg
import sys
import time

import numpy as np
import numpy.random as rnd
import networkx as nx

#%%
pg.init()

screen_size = (800,600) 
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Random graphs with PyGame")
finish = False

#%%
# pick a random geometric graph
def get_geom_graph(screen):
    n = 100
    pos = {i: (rnd.randint(1, screen.get_size()[0]), rnd.randint(1,
        screen.get_size()[1])) for i in range(n+1)}
    rad = 2*(np.sqrt(screen.get_size()[0]) + np.sqrt(screen.get_size()[1]))
    g = nx.random_geometric_graph(n, rad, pos=pos)
    return g


def draw_geom_graph(screen, graph):

    #%%
    # draw the graph
    
    # draw nodes
    for n in graph.nodes:
        color = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
        position = (graph.nodes[n]['pos'][0], graph.nodes[n]['pos'][1])
        pg.draw.circle(screen, color, position, 1)
        pg.display.update()

    # draw edges
    for e in graph.edges:
        color = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
        start_position = tuple(graph.nodes[e[0]]['pos'])
        end_position = tuple(graph.nodes[e[1]]['pos'])
        pg.draw.line(screen, color, start_position, end_position, 1)
        time.sleep(0.005)
        pg.display.update()


# start with a first graph
g = get_geom_graph(screen)
draw_geom_graph(screen, g)

#%% 
# main loop
while not finish:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finish = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # draw new graph
                g = get_geom_graph(screen)
                draw_geom_graph(screen, g)
            if event.key == pg.K_f:
                pg.display.toggle_fullscreen()
            elif event.key == pg.K_q:
                # quit after pressing Q
                finish = True
            elif event.key == pg.K_c:
                # clear the screen
                screen.fill((0,0,0))
                pg.display.update()
                     
sys.exit()
