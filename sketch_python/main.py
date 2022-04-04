import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm 
from mpl_toolkits.mplot3d import Axes3D 
from Particle import Particle
from config import PARTICLES_AMOUNT
# from config import *


# NOT USED AT THE MOMENT
# C1 = 10
# C2 =  5 # learning factors (C1: own, C2: social) (ok)
# evals = 0
# evals_to_best = 0 #número de evaluaciones, sólo para despliegue

particles = []# arreglo de partículas

fig = plt.figure() 
ax = fig.gca(projection="3d")

# Stop program hanging after pressing esc
def on_close(event):
  quit()

fig.canvas.mpl_connect('close_event', on_close)

# Setup Rastrigin plot, initialize particles
def setup():
  X = np.linspace(-5.12, 5.12, 100)     
  Y = np.linspace(-5.12, 5.12, 100)     
  X, Y = np.meshgrid(X, Y) 

  Z = (X**2 - 10 * np.cos(2 * np.pi * X)) + \
    (Y**2 - 10 * np.cos(2 * np.pi * Y)) + 20
  
  ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
    cmap=cm.nipy_spectral, linewidth=0.08,
    antialiased=True) 

  ax.view_init(elev=90)
  
  for i in range(PARTICLES_AMOUNT):
    particle = Particle()
    particles.append(particle)

  plt.draw()
  # plt.savefig('rastrigin_graph.png')

def draw_best():
  ax.plot(Particle.g_best_x, Particle.g_best_y, 100, marker="x", markersize=10, markerfacecolor="white", markeredgecolor="white", zorder=101)

def draw_particle(particle):
  ax.plot(particle.x, particle.y, 100, marker="o", markersize=3, markerfacecolor="black", markeredgecolor="black", zorder=101)

setup()


# Main loop
while True:
  plt.draw()
  # Delete old point graphics
  for i,line in enumerate(ax.get_lines()):
    # print("removing line")
    line.remove()
  # print("Lines removed")
  # Move points, eval and draw to new locations
  for i in range(len(particles)):
    particles[i].move()
    particles[i].eval()
    draw_particle(particles[i])
  # Draw new (or same) best
  draw_best()
  plt.pause(0.0001)

