# BOTH
PARTICLES_AMOUNT = 100
RUNS_PER_SIMULATION = 250
RASTRIGIN_MIN = -5.12
RASTRIGIN_MAX = 5.12

# PSO
MAX_V = 0.6 # max velocidad (modulo)
INERCIA = 25 # inercia: baja (~50): explotación, alta (~5000): exploración (2000 ok)
C1 = 25 # learning factors (C1: own, C2: social)
C2 = 25

# GA
PARENT_PARTICLES_AMOUNT = 80 # Has to be lower than PARTICLES_AMOUNT
CHANCE_TO_MUTATE_PERCENTAGE = 75 
MUTATE_WEIGHT = 1 # GA inercia


