import sys
import numpy as np
from config import *

class Particle:
  g_best = sys.float_info.max # Global best fit, init to max to reset at first fit
  # Global best pos
  g_best_x = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX) 
  g_best_y = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)

  #  ---------------------------- Constructor
  def __init__(self, x, y):
    # Current pos
    self.x = x
    self.y = y
    # Personal best pos
    self.py = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)
    self.px = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    # Current velocity
    self.vx = np.random.uniform(-1,1)
    self.vy = np.random.uniform(-1,1)
    # Personal best fit
    self.pfit = 100000
    # Current fit
    self.fit = 100000
  
  
  # Evaluate fit, if new global best is found, return True
  def eval(self): #recibe imagen que define función de fitness
    self.fit = self.evalPos() #evalúa por el valor de la componente roja de la imagen
    if(self.fit < self.pfit): # actualiza local best si es mejor
      self.pfit = self.fit
      self.px = self.x
      self.py = self.y
    if (self.fit < Particle.g_best): # actualiza global best
      Particle.g_best = self.fit
      Particle.g_best_x = self.x
      Particle.g_best_y = self.y
      return True
    return False
  
  
  def evalPos(self): 
    return (self.x**2 - 10 * np.cos(2 * np.pi * self.x)) + \
  (self.y**2 - 10 * np.cos(2 * np.pi * self.y)) + 20
  
  # def calculate(self, val):
  #   return pow(val, 2) - 10 * np.cos(2*PI*val) 
  
  
  # ------------------------------ mueve la partícula
  def move_pso(self):
    rand = np.random
    # === Actualiza velocidad (fórmula con factores de aprendizaje C1 y C2) ===
    # self.vx = self.vx + rand.uniform(0,1)*C1*(self.px - self.x) + rand.uniform(0,1)*C2*(Particle.g_best_x - self.x)
    # self.vy = self.vy + rand.uniform(0,1)*C1*(self.py - self.y) + rand.uniform(0,1)*C2*(Particle.g_best_y - self.y)

    # === Actualiza velocidad (fórmula con inercia, p.250) ===
    # self.vx = INERCIA * self.vx + rand.uniform(0,1)*(self.px - self.x) + rand.uniform(0,1)*(Particle.g_best_x - self.x)
    # self.vy = INERCIA * self.vy + rand.uniform(0,1)*(self.py - self.y) + rand.uniform(0,1)*(Particle.g_best_y - self.y)

    # ==== Actualiza velocidad (fórmula mezclada) ====
    self.vx = INERCIA * self.vx + rand.uniform(0,1)*C1*(self.px - self.x) + rand.uniform(0,1)*C2*(Particle.g_best_x - self.x)
    self.vy = INERCIA * self.vy + rand.uniform(0,1)*C1*(self.py - self.y) + rand.uniform(0,1)*C2*(Particle.g_best_y - self.y)
    # trunca velocidad a maxv
    modu = np.sqrt(self.vx*self.vx + self.vy*self.vy)
    if (modu > MAX_V):
      self.vx = self.vx/modu*MAX_V
      self.vy = self.vy/modu*MAX_V
 
    # Update position
    temp_new_x = self.x + self.vx
    temp_new_y = self.y + self.vy
    # Change velocity to opposite if going over limits
    if (temp_new_x > RASTRIGIN_MAX or temp_new_x < RASTRIGIN_MIN): self.vx = - self.vx
    if (temp_new_y > RASTRIGIN_MAX or  temp_new_y< RASTRIGIN_MIN): self.vy = - self.vy
    self.x = self.x + self.vx
    self.y = self.y + self.vy