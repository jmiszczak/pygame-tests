# Visualization of Q-learning algorithm for the Frozen Lake game
# Author: Jarosław Miszczak <jarek@miszczak.eu>
# NOTE: To run this script you need to install networkx and pygame

import sys
import time

import networkx as nx
import random as rnd
import pygame as pg
import numpy as np

# game board
board = [
        "SFFF",
        "FHHF",
        "FFHF",
        "HFFG"
        ]

# colors and fonts
RED = (255,0,0,64)
GREEN = (0,255,0,128)
BLUE = (0,0,255,128)
YELLOW = (255,255,0,0) 
LINE = (255,0,0)
field_color = { 'S': YELLOW, 'G': GREEN, 'F' : BLUE, 'H' : RED }
font_size = 40
info_font_size = 22
field_size = font_size + 25

# grid for playing
grid = nx.grid_2d_graph(4,4)
for n in grid.nodes:
    grid.nodes[n]['s'] = board[n[0]][n[1]]

# learning settings
# NOTE: only random exploration is implemented
# 
rate = 1
gamma = 0.5
episode = 0
max_steps = 100
batch_episodes = 100

# Q table is indexed by the edges
Q = {}

# restart - clear the Q table and episode counter
def restart_agent():
    global episode 
    episode = 0
    for e in grid.edges:
        Q[e] = 0
        Q[tuple(reversed(e))] = 0

# play single episode of the game
def single_episode():
    global episode
    episode = episode + 1
    # single episode
    # we start the game
    play = True
    # we start in 'S' at (0,0)
    state = (0,0)
    reward  = 0

    #print("[INFO] Episode", ep)
    while play:
        # get one of the neighbors
        # they are selected uniformly random
        old_state = state
        new_state = rnd.choice(list(grid.neighbors(old_state)))
        state = new_state
    
        # are we done or no?
        ls = grid.nodes[new_state]['s']
        if ls in ['H', 'G']:
            play = False
            if ls == 'G':
                reward = 1

        # update values in the Q table
        # based on https://en.wikipedia.org/wiki/Q-learning
        Q[(old_state,new_state)] = Q[(old_state,new_state)] \
                + rate*(reward + gamma * max(Q[(new_state,nn)] for nn in grid.neighbors(new_state)) \
                            - Q[(old_state,new_state)])
    
    # display current values in Q table 
    print("Episode", episode)
    for e in grid.edges:
        print('Edged', e, 'has Q value', Q[e])

# two methods for the visualization of the current value in Q table
# method 1: line width - problematic for small values
def line_size(qval, Q):
    # q_vals = list(set(Q.values()))
    # q_vals.sort()
    # if qval > 0 :
    #     return 3*q_vals.index(qval)
    # else:
    #     return 1
    if qval > 0 :
        # we assume 10 possible line widths
        q_vals = [ _/9 for _ in range(11) ]
        # print(q_vals)
        return 3*[q_vals.index(_) for _ in q_vals if _ > qval][0]
    else :
        return 0
    

# method 2: alpha in the color specification
def line_alpha(qval):
    if qval > 0 :
        return 64+(255-64)*qval
    else :
        return 0

# illustration of the Frozen Lake
def draw_board(screen):
    
    # calculate screen coordinates 
    x,y = int(screen_size[0]/4), int(screen_size[1]/4)
    
    # draw lines between the fields to illustrate the connectivity
    # NOTE: this is not used as the line width is set to zero
    for e in grid.edges:
        spos = ( int((0.5+e[0][0])*x), int((0.5+e[0][1])*y) )
        epos = ( int((0.5+e[1][0])*x), int((0.5+e[1][1])*y) )
        # change 0 to 1 to see lines
        pg.draw.line(screen, (128,128,128,128), spos, epos, 0)

    # display field name
    for n in grid.nodes:
        npos = ( int((0.5+n[1])*x-font_size/4), int((0.5+n[0])*y-font_size/4) )
        rpos = ( int((0.5+n[1])*x-field_size/2), int((0.5+n[0])*y-field_size/2) )
        if grid.nodes[n]['s'] in ['S'] :
            img = font.render(grid.nodes[n]['s'], True, (255,0,255))
        else :
            img = font.render(grid.nodes[n]['s'], True, (255,255,255))
        pg.draw.rect(screen, field_color[grid.nodes[n]['s']], pg.Rect(rpos,(field_size,field_size)), 0)
        screen.blit(img, npos)

    # redraw
    pg.display.update()

# redraw lines according to Q table
def update_board(screen, alpha=True):

    # update episode information
    screen.fill((255,255,255))
    font = pg.font.SysFont(None, info_font_size)
    img = font.render('Current episode: ' + str(episode), True, (0,0,255))
    screen.blit(img, (10, 0.95*screen_size[1]))
    pg.display.update()
    
    # calculate screen coordinates 
    x, y = int(screen_size[0]/4), int(screen_size[1]/4)
   
    # add lines visualizing Q values
    if not alpha:
        # method 1: Q values used to calculate line width
        for e in grid.edges:
            spos = ( int((0.5+e[0][1])*x), int((0.5+e[0][0])*y) )
            epos = ( int((0.5+e[1][1])*x), int((0.5+e[1][0])*y) )
            pg.draw.line(screen, LINE, spos, epos, line_size(Q[e], Q)) 
    else :
        # method 2: Q values used to change alpha of the lines
        for e in grid.edges:
            spos = ( int((0.5+e[0][1])*x)-(line_size(Q[e],Q)-1)/2,
                    int((0.5+e[0][0])*y)-(line_size(Q[e],Q)-1)/2)
            epos = ( int((0.5+e[1][1])*x)-(line_size(Q[e],Q)-1)/2,
                    int((0.5+e[1][0])*y)-(line_size(Q[e],Q)-1)/2)
            if spos[0] == epos[0] : # horizontal line
                line = pg.Surface((line_size(Q[e], Q), abs(spos[1]-epos[1])), pg.SRCALPHA)
                line.fill( LINE + (line_alpha(Q[e]),))
                screen.blit(line, spos)
            elif spos[1] == epos[1] : # vertical line
                line = pg.Surface((abs(spos[0]-epos[0]), line_size(Q[e], Q)), pg.SRCALPHA)
                line.fill(LINE + (line_alpha(Q[e]), ))
                screen.blit(line, spos)
            else :
                print ("[INFO] Problem with line coordinates.")

            # add values for reversed edges
            e = tuple(reversed(e))
            if spos[0] == epos[0] : # horizontal line
                line = pg.Surface((line_size(Q[e], Q), abs(spos[1]-epos[1])), pg.SRCALPHA)
                line.fill( LINE + (line_alpha(Q[e]),))
                screen.blit(line, spos)
            elif spos[1] == epos[1] : # vertical line
                line = pg.Surface((abs(spos[0]-epos[0]), line_size(Q[e], Q)), pg.SRCALPHA)
                line.fill( LINE + (line_alpha(Q[e]),))
                screen.blit(line, spos)
            else :
                print ("[INFO] Problem with line coordinates.")


    # draw the fields
    draw_board(screen)

    # redraw
    pg.display.update()

#
# screen initialization
#
pg.init()
screen_size = (500, 500) 
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Frozen Lake Demo")
screen.fill((255,255,255))

#
# welcome screen 
#
font = pg.font.SysFont(None, font_size)
imgs = [ font.render('Keyboard controls', True, BLUE),
        font.render('p: play ' + str(batch_episodes) + ' episodes', True, BLUE),
        font.render('e: play single episode', True, BLUE),
        font.render('r: restart', True, BLUE),
        font.render('q: quit', True, BLUE)
        ]
for i, img in enumerate(imgs):
    screen.blit(img, (20, 20+i*1.5*info_font_size))
pg.display.update()

#
# main loop
#
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
            elif event.key == pg.K_p:
                screen.fill((255,255,255))
                if episode == 0:
                    restart_agent()
                    draw_board(screen)
                for _ in range(batch_episodes):
                    single_episode()
                    update_board(screen)
                    time.sleep(0.01)
            elif event.key == pg.K_e:
                screen.fill((255,255,255))
                if episode == 0:
                    restart_agent()
                    draw_board(screen)
                single_episode()
                update_board(screen)
            elif event.key == pg.K_r:
                # restart the agent
                restart_agent()
                # draw clear board
                screen.fill((255,255,255))
                draw_board(screen)

sys.exit()
