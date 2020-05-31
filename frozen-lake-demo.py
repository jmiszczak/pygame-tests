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

RED = (255,0,0,64)
GREEN = (0,255,0,128)
BLUE = (0,0,255,128)
YELLOW = (255,255,0,0) 
LINE = (82,82,82,128)
field_color = { 'S': YELLOW, 'G': GREEN, 'F' : BLUE, 'H' : RED }
font_size = 32

# grid for playing
grid = nx.grid_2d_graph(4,4)
for n in grid.nodes:
    grid.nodes[n]['s'] = board[n[0]][n[1]]

# learning settings
#
rate = 1
gamma = 0.5
episode = 0
batch_episodes = 50
# Q table
Q = {}

def restart_agent():
    global episode 
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
        print('Edged', e, 'has Q value', Q[e])

# visualization of the current value in Q table 
def line_size(qval):
    if qval > 0.0:
        return int(3*(6+np.log2(qval)))
    else:
        return 0

# illustration of the Frozen Lake
def draw_board(screen):
    
    x,y = int(screen_size[0]/4), int(screen_size[1]/4)
    field_size = font_size + 8
    font = pg.font.SysFont(None, font_size)
 
    # draw lines  between the fields to illustrate the connectivity
    for e in grid.edges:
        spos = ( int((0.5+e[0][0])*x), int((0.5+e[0][1])*y) )
        epos = ( int((0.5+e[1][0])*x), int((0.5+e[1][1])*y) )
        pg.draw.line(screen, (128,128,128,128), spos, epos, 0)

    # display filed name
    for n in grid.nodes:
        npos = ( int((0.5+n[1])*x-font_size/4), int((0.5+n[0])*x-font_size/4) )
        rpos = ( int((0.5+n[1])*x-field_size/2), int((0.5+n[0])*x-field_size/2) )
        if grid.nodes[n]['s'] in ['S'] :
            img = font.render(grid.nodes[n]['s'], True, (255,0,255))
        else :
            img = font.render(grid.nodes[n]['s'], True, (255,255,255))
        pg.draw.rect(screen, field_color[grid.nodes[n]['s']], pg.Rect(rpos,(field_size,field_size)), 0)
        screen.blit(img, npos)


    pg.display.update()

# redraw lines according to Q table
def update_board(screen):

    screen.fill((255,255,255))
    font = pg.font.SysFont(None, font_size)
    img = font.render('Current episode: ' + str(episode), True, (0,0,255))
    screen.blit(img, (20, 20))
    pg.display.update()
    
    x,y = int(screen_size[0]/4), int(screen_size[1]/4)
    for e in grid.edges:
        spos = ( int((0.5+e[0][1])*x), int((0.5+e[0][0])*y) )
        epos = ( int((0.5+e[1][1])*x), int((0.5+e[1][0])*y) )
        pg.draw.line(screen, LINE, spos, epos, line_size(Q[e])) 
    draw_board(screen)
    pg.display.update()

#
# PyGame screen initialization
#
pg.init()
screen_size = (800, 800) 
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Frozen Lake Demo")
screen.fill((255,255,255))

#
# welcome screen 
#
font = pg.font.SysFont(None, font_size)
img1 = font.render('Keyboard controls', True, BLUE)
img2 = font.render('p: play ' + str(batch_episodes) + ' episodes, e: play single episode, r: restart, q:quit', True, BLUE)
screen.blit(img1, (20, 20))
screen.blit(img2, (20, 20+font_size))
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
                pg.display.update()
         
    pg.display.update()

sys.exit()
