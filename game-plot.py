import pygame
from pygame.locals import *

import matplotlib
import matplotlib.figure as figure
import matplotlib.backends.backend_agg as agg
matplotlib.use("Agg")

t, s = [1, 2, 4], [1, 4/10, 8/10]
t, v = [1, 2, 3], [2, 8, 14]
def plot_data(time,dist, vel):
    fig = figure.Figure(figsize=[4, 3], dpi=100)
    fig.patch.set_alpha(0.1)

    ax1 = fig.add_subplot(121)
    ax1.set_xlim([0, 100])
    ax1.set_ylim([0, 1000])
    ax1.plot(time,dist, color='red')
    ax1.set_title('Velocity v(t)')

    ax2 = fig.add_subplot(122)
    ax2.plot(time,vel, color='green')
    ax2.set_title('Distance s(t)')
    ax2.set_xlim([0, 100])
    ax2.set_ylim([0, 1000])
 
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()
    return canvas, raw_data

pygame.init()

window = pygame.display.set_mode((800, 800), DOUBLEBUF)
screen = pygame.display.get_surface()
bg_color = (255, 0, 0)   # fill red as background color
screen.fill(bg_color)


stop = False
while not stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True

    # tutaj jest kontrola autka
    t.append(t[-1]+1)
    v.append(1/2*t[-1])
    s.append(1/10*t[-1]**2)

    # rysowanie danych
    canvas, raw_data = plot_data(t,s,v)
    size = canvas.get_width_height()
    surf = pygame.image.frombuffer(raw_data, size, "RGBA")
    screen.blit(surf, (300, 5))  # x, y position on screen
    pygame.display.flip()
    screen.fill(bg_color)

    pygame.time.Clock().tick(10)  # Avoid 100% CPU usage
