import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm 
from mpl_toolkits.mplot3d import Axes3D 
from Particle import Particle
from config import *

rand = np.random

# NOT USED AT THE MOMENT
# C1 = 10
# C2 =  5 # learning factors (C1: own, C2: social) (ok)
# evals = 0
# evals_to_best = 0 #número de evaluaciones, sólo para despliegue

# ==== MODE ====
is_pso = True # True for PSO, False for GA
# ==============

particles = []
# For example with 60% MUTATION_PERCENTAGE this gives random range of (0.7, 1.3)
ga_mutation_bottom = 1 - (MUTATION_PERCENTAGE / 100 / 2)
ga_mutation_top = 1 + (MUTATION_PERCENTAGE / 100 / 2)

fig = plt.figure() 
ax = fig.gca(projection="3d")

# Stop program hanging after pressing esc
def on_close(event):
  quit()

fig.canvas.mpl_connect('close_event', on_close)

# Setup Rastrigin plot, initialize particles
def setup():
  if (is_pso == False and PARTICLES_AMOUNT < BEST_PARTICLES_AMOUNT):
    print("PARTICLES_AMOUNT is lower than BEST_PARTICLES_AMOUNT, change your config. Quitting.")
    quit()
  print("Starting simulation in " + ("PSO" if is_pso == True else "GA"))
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
    start_x = rand.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    start_y = rand.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    particle = Particle(start_x, start_y)
    particles.append(particle)
    particle.eval()

  plt.draw()

def draw_best():
  ax.plot(Particle.g_best_x, Particle.g_best_y, 100, marker="x", markersize=10, markerfacecolor="white", markeredgecolor="white", zorder=101)

def draw_particle(particle):
  ax.plot(particle.x, particle.y, 100, marker="o", markersize=3, markerfacecolor="black", markeredgecolor="black", zorder=101)

setup()


# Main loop
while True:
  plt.draw()
  print("WHILE LOOP, is_pso: " + str(is_pso))
  # Delete old point graphics
  for i,line in enumerate(ax.get_lines()):
    line.remove()

  # PSO simulation
  if (is_pso):
    # Move points, eval and draw to new locations
    for i in range(len(particles)):
      particles[i].move_pso()
      particles[i].eval()
      draw_particle(particles[i])
  # GA simulation
  else:
    # 1. Sort particles by best fits
    particles.sort(key=lambda x: x.fit)
    best_particles = particles[:BEST_PARTICLES_AMOUNT]
    bp = best_particles[0]
    print("Best particle x: %d, y: %d, fit: %d", bp.x, bp.y, bp.fit)
    # Delete old particles
    particles = []
    # 2. Take genes (which genes?) of x best particles
    best_x_genes = []
    best_y_genes = []
    for p in best_particles:
      best_x_genes.append(p.x)
      best_y_genes.append(p.y)

    # 3. Generate new particles from these genes, add random mutation
    for i in range(PARTICLES_AMOUNT):
      # Select new genes by random from best genes and mutate these genes
      new_x = rand.choice(best_x_genes) * rand.uniform(ga_mutation_bottom, ga_mutation_top) + (rand.uniform(-1, 1) * RANDOM_WEIGHT)
      new_y = rand.choice(best_y_genes) * rand.uniform(ga_mutation_bottom, ga_mutation_top) + (rand.uniform(-1, 1) * RANDOM_WEIGHT)

      new_particle = Particle(new_x, new_y)
    # 4. Eval new particles
      new_particle.eval()
      particles.append(new_particle)
    # 5. Draw new particles
      draw_particle(new_particle)
    
  # TODO: Objective function, when to stop?
      
  # Draw new (or same) best
  draw_best()
  plt.pause(0.01)

