import sys
import time

import networkx as nx
import random as rnd
import pygame as pg
import numpy as np

# game board
board = [
        "SFFF",
        "FHFH",
        "FFFH",
        "HFFG"
        ]

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
# grid for playing
grid = nx.grid_2d_graph(4,4)
for n in grid.nodes:
    grid.nodes[n]['s'] = board[n[0]][n[1]]

# learning settings
#
rate = 1
gamma = 0.5
episode = 0
# Q table
Q = {}

def restart_agent():
    episode = 0
    for e in grid.edges:
        Q[e] = 0
        Q[tuple(reversed(e))] = 0

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
        old_state = state
        new_state = rnd.choice(list(grid.neighbors(old_state)))
        state = new_state
    
        # are we done or no?
        ls = grid.nodes[new_state]['s']
        if ls in ['H', 'G']:
            play = False
            if ls == 'G':
                reward = 1
        Q[(old_state,new_state)] = Q[(old_state,new_state)] \
                + rate*(reward + gamma * max(Q[(new_state,nn)] for nn in grid.neighbors(new_state)) \
                            - Q[(old_state,new_state)])
    
    print("Episode", episode)
    for e in grid.edges:
        print(e, Q[e])

def draw_board(screen):

    font = pg.font.SysFont(None, 24)
    img = font.render('episode:' + str(episode), True, (0,0,255))
    screen.blit(img, (20, 20))
    pg.display.update()
    
    x,y = int(screen_size[0]/4), int(screen_size[1]/4)
    for e in grid.edges:
        spos = ( int((0.5+e[0][0])*x), int((0.5+e[0][1])*y) )
        epos = ( int((0.5+e[1][0])*x), int((0.5+e[1][1])*y) )
        pg.draw.circle(screen, RED, spos, 10)
        pg.draw.circle(screen, RED, epos, 10)
        pg.draw.line(screen, BLUE, spos, epos, int(32*Q[e]))
    pg.display.update()

#%%
pg.init()

width, height = 800, 600
screen_size = (width, height) 
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Frozen Lake Demo")
screen.fill((255,255,255))
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
                restart_agent()
                for _ in range(500):
                    single_episode()
                    draw_board(screen)
                    time.sleep(0.05)
            elif event.key == pg.K_e:
                if episode == 0:
                    restart_agent()
                single_episode()
                draw_board(screen)
            elif event.key == pg.K_r:
                # clear the screen
                restart_agent()
                screen.fill((255,255,255))
                pg.display.update()
         
#    color = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
#    position = (rnd.randint(1,screen_size[0]), rnd.randint(1, screen_size[1]))
#    pg.draw.circle(screen, color, position, 5)
    pg.display.update()

sys.exit()
