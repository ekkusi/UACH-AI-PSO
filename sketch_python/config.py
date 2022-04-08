# BOTH
PARTICLES_AMOUNT = 50

# PSO
RASTRIGIN_MIN = -5.12
RASTRIGIN_MAX = 5.12
INERCIA = 30 # inercia: baja (~50): explotación, alta (~5000): exploración (2000 ok)
MAX_V = 1 # max velocidad (modulo)
C1 = 30 # learning factors (C1: own, C2: social)
C2 = 10 

# GA
BEST_PARTICLES_AMOUNT = 10 # Has to be lower than PARTICLES_AMOUNT
MUTATION_PERCENTAGE = 150
RANDOM_WEIGHT = 0.5