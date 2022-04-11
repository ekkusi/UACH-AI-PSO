# BOTH
PARTICLES_AMOUNT = 100
RUNS_PER_SIMULATION = 100

# PSO
RASTRIGIN_MIN = -5.12
RASTRIGIN_MAX = 5.12
INERCIA = 20 # inercia: baja (~50): explotación, alta (~5000): exploración (2000 ok)
MAX_V = 0.5 # max velocidad (modulo)
C1 = 10 # learning factors (C1: own, C2: social)
C2 = 30 

# GA
BEST_PARTICLES_AMOUNT = 10 # Has to be lower than PARTICLES_AMOUNT
MUTATION_RANGE_PERCENTAGE= 150
CHANCE_TO_MUTATE_PERCENTAGE = 50
RANDOM_WEIGHT = 0.7 # GA inercia
