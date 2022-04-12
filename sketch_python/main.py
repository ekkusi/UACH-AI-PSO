from hashlib import sha3_224
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm 
from mpl_toolkits.mplot3d import Axes3D 
from Particle import Particle
from config import *
import random as rand
import json
import os

script_dir = os.path.dirname(__file__)
results_file_path = os.path.join(script_dir, "results.json")
# NOT USED AT THE MOMENT
# C1 = 10
# C2 =  5 # learning factors (C1: own, C2: social) (ok)
# evals = 0
# evals_to_best = 0 #número de evaluaciones, sólo para despliegue

# ==== MODE ====
is_pso = False # True for PSO, False for GA
with_graphics = False # False for faster running of simulations, only prints
# ==============

particles = []
# For example with 60% MUTATION_PERCENTAGE this gives random range of (0.7, 1.3)
# ga_mutation_bottom = 1 - (MUTATION_RANGE_PERCENTAGE / 100 / 2)
# ga_mutation_top = 1 + (MUTATION_RANGE_PERCENTAGE / 100 / 2)


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
  global particles
  Particle.reset_globals()
  if (is_pso == False and PARTICLES_AMOUNT < PARENT_PARTICLES_AMOUNT):
    print("PARTICLES_AMOUNT is lower than PARENT_PARTICLES_AMOUNT, change your config. Quitting.")
    quit()
  particles = []
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



def simulate():
  global particles
  evals_to_best = 0
  # Main simulation loop
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
      # 1. Select next gen parents randomly from particles with probabilities of being selected being weighted by fit value
      particle_fits = list(map(lambda p: 1/p.fit, particles))
      best_particles = rand.choices(particles, weights=particle_fits, k=PARENT_PARTICLES_AMOUNT)
      particle_fits.sort()
      best_particles.sort(key=lambda p: p.fit)
      particles.clear()

      # print("Best fits: " + ", ".join([str(p) for p in particle_fits]))
      # print("All: " + ", ".join([str(p.fit) for p in best_particles]))

      # 2. Take genes (which genes?) of x best particles
      best_x_genes = []
      best_y_genes = []
      for p in best_particles:
        best_x_genes.append(p.x)
        best_y_genes.append(p.y)
        # Add best particles (parents) to compete for new generation by default
        particles.append(p)

      # 3. Cross new particles from the parents x and y, after we have PARENT_PARTICLES_AMOUNT + PARTICLES_AMOUNT particles
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
          p.x = p.x + (rand.uniform(-1, 1) * MUTATE_WEIGHT) 
          p.y = p.y + (rand.uniform(-1, 1) * MUTATE_WEIGHT)
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

    # print("ROUND: %d, best fit: %d, rounds to best: %d", round, Particle.g_best, evals_to_best)
  return {"rounds_to_best": evals_to_best, "best_fit": Particle.g_best }

setup()
print("Starting simulation in " + ("PSO" if is_pso == True else "GA"))

# Only simulate once if with graphics and don't write to json 
if with_graphics: 
  simulate()
  print("Simulation over")
# Run simulation x times (number in loop) and write results to results.json
else:
  simulation_results = []
  result = {
    "mode": "PSO" if is_pso == True else "EA",
    "particles_amount": PARTICLES_AMOUNT,
    "runs_per_simulation": RUNS_PER_SIMULATION
  }
  if is_pso == True:
    result["inercia"] = INERCIA
    result["max_v"] = MAX_V
    result["c1"] = C1
    result["c2"] = C2
  else:
    result["parent_particles_amount"] = PARENT_PARTICLES_AMOUNT
    result["change_to_mutate_percentage"] = CHANCE_TO_MUTATE_PERCENTAGE
    result["mutate_weight"] = MUTATE_WEIGHT
  best_result = None
  for i in range(10): # Change this value to change the numbers of simulations run per configuration
    sim_result = simulate()
    if (best_result == None or best_result["best_fit"] < sim_result["best_fit"]): best_result = sim_result
    simulation_results.append(sim_result)
    setup() # Reset stuff after each simulation
    print("Simulation ", i, " complete, best fit found: " + str(sim_result["best_fit"])+ " in the round: " + str(sim_result["rounds_to_best"]))
  print("Simulations complete, writing json")
  best_fits = list(map(lambda r: r["best_fit"], simulation_results))
  rounds_to_best_list = list(map(lambda r: r["rounds_to_best"], simulation_results))
  best_fit_average = np.average(best_fits)
  rounds_to_best_average = np.rint(np.average(rounds_to_best_list))
  result["best_fit_average"] = best_fit_average
  result["rounds_to_best_average"] = best_fit_average
  result["simulation_results"] = simulation_results

  data = None
  with open(results_file_path) as json_file:
    data = json.load(json_file)
    if not "results" in data: data["results"] = []
    data["results"].append(result)
    print("Json data read")
  with open(results_file_path, "w") as outfile:
    json_string = json.dumps(data, indent=4)
    outfile.write(json_string)
    print("Json data written")


quit()
