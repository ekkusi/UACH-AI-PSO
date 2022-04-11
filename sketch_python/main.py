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
with_graphics = True
# ==============

particles = []
# For example with 60% MUTATION_PERCENTAGE this gives random range of (0.7, 1.3)
ga_mutation_bottom = 1 - (MUTATION_RANGE_PERCENTAGE / 100 / 2)
ga_mutation_top = 1 + (MUTATION_RANGE_PERCENTAGE / 100 / 2)

evals_to_best = 0

# Stop program hanging after pressing esc
def on_close(event):
  quit()

fig = None
ax = None
if with_graphics:
  fig = plt.figure() 
  ax = fig.gca(projection="3d")
  fig.canvas.mpl_connect('close_event', on_close)



# Setup Rastrigin plot, initialize particles
def setup():
  if (is_pso == False and PARTICLES_AMOUNT < BEST_PARTICLES_AMOUNT):
    print("PARTICLES_AMOUNT is lower than BEST_PARTICLES_AMOUNT, change your config. Quitting.")
    quit()
  print("Starting simulation in " + ("PSO" if is_pso == True else "GA"))
  for i in range(PARTICLES_AMOUNT):
    start_x = rand.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    start_y = rand.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    particle = Particle(start_x, start_y)
    particles.append(particle)
    particle.eval()

  if with_graphics:
    X = np.linspace(-5.12, 5.12, 100)     
    Y = np.linspace(-5.12, 5.12, 100)     
    X, Y = np.meshgrid(X, Y) 

    Z = (X**2 - 10 * np.cos(2 * np.pi * X)) + \
      (Y**2 - 10 * np.cos(2 * np.pi * Y)) + 20
    
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
      cmap=cm.nipy_spectral, linewidth=0.08,
      antialiased=True) 

    ax.view_init(elev=90)

    plt.draw()
  


def draw_best():
  ax.plot(Particle.g_best_x, Particle.g_best_y, 100, marker="x", markersize=10, markerfacecolor="white", markeredgecolor="white", zorder=101)

def draw_particle(particle):
  ax.plot(particle.x, particle.y, 100, marker="o", markersize=3, markerfacecolor="black", markeredgecolor="black", zorder=101)

setup()


# Main loop
for round in range(RUNS_PER_SIMULATION):
  if with_graphics:
    plt.draw()
    # Delete old point graphics
    for i,line in enumerate(ax.get_lines()):
      line.remove()

  # PSO simulation
  if is_pso:
    # Move points, eval and draw to new locations
    for i in range(len(particles)):
      particles[i].move_pso()
      if particles[i].eval(): # If eval returns true, new global best is found
        evals_to_best = round
      if with_graphics: draw_particle(particles[i])
  # GA simulation
  else:
    # 1. Sort particles by best fits and select BEST_PARTICLES_AMOUNT of the best as parents to next gen
    # TODO?: Select parents from all particles but with a weighted probability of being selected determined by fit. Could use random-library choices method.
    particles.sort(key=lambda x: x.fit)
    best_particles = particles[:BEST_PARTICLES_AMOUNT]
    particles = [] # Delete old gene

    # 2. Take genes (which genes?) of x best particles
    best_x_genes = []
    best_y_genes = []
    for p in best_particles:
      best_x_genes.append(p.x)
      best_y_genes.append(p.y)
      # Add best particles (parents) to compete for new generation by default
      particles.append(p)

    # 3. Cross new particles from the parents x and y, after we have BEST_PARTICLES_AMOUNT + PARTICLES_AMOUNT particles
    for i in range(PARTICLES_AMOUNT):
      # Select new genes by random from best genes 
      new_x = rand.choice(best_x_genes) 
      new_y = rand.choice(best_y_genes) 
    
      new_particle = Particle(new_x, new_y)
      particles.append(new_particle)

    # 4. Mutation for all particles, children and old generation parents and evaluate after
    for p in particles:
      if rand.uniform(0,1) < CHANCE_TO_MUTATE_PERCENTAGE / 100:
        # Mutation == Add random number from the range  {-RANDOM_WEIGHT, RANDOM_WEIGHT} * to both x and y
        p.x = p.x + (rand.uniform(-1, 1) * RANDOM_WEIGHT) 
        p.y = p.y + (rand.uniform(-1, 1) * RANDOM_WEIGHT)
      if p.eval():
        evals_to_best = round
    
    # 5. Evolution, compete all crossed and mutated particles (children and old gen parents) and let only the fittest survive
    particles.sort(key=lambda x: x.fit)
    particles = particles[:PARTICLES_AMOUNT]

    if with_graphics:
      # 6. Draw new particles
      for p in particles:
        draw_particle(p)

    
  # TODO: Objective function, when to stop?
      
  # Draw new (or same) best
  if with_graphics:
    draw_best()
    plt.pause(0.001)

  print("ROUND: %d, best fit: %d, rounds to best: %d", round, Particle.g_best, evals_to_best)

print("Simulation over, global best: %d, found in %d rounds", Particle.g_best, evals_to_best)
quit()
