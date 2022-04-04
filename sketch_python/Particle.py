import numpy as np
from config import *

class Particle:
  g_best = 100000
  g_best_x = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)
  g_best_y = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)

  #  ---------------------------- Constructor
  def __init__(self):
    self.x = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    self.y = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    self.py = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    self.px = np.random.uniform(RASTRIGIN_MIN, RASTRIGIN_MAX)   
    self.vx = np.random.uniform(-1,1)
    self.vy = np.random.uniform(-1,1)
    self.pfit = 100000
    self.fit = 100000
  
  
  # ---------------------------- Evalúa partícula
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
  
  
  def evalPos(self): 
    return (self.x**2 - 10 * np.cos(2 * np.pi * self.x)) + \
  (self.y**2 - 10 * np.cos(2 * np.pi * self.y)) + 20
  
  # def calculate(self, val):
  #   return pow(val, 2) - 10 * np.cos(2*PI*val) 
  
  
  # ------------------------------ mueve la partícula
  def move(self):
    #actualiza velocidad (fórmula con factores de aprendizaje C1 y C2)
    #vx = vx + random(0,1)*C1*(px - x) + random(0,1)*C2*(gbestx - x)
    #vy = vy + random(0,1)*C1*(py - y) + random(0,1)*C2*(gbesty - y)
    #actualiza velocidad (fórmula con inercia, p.250)
    random = np.random
    self.vx = INERCIA * self.vx + random.randint(1)*(self.px - self.x) + random.randint(1)*(Particle.g_best_x - self.x)
    self.vy = INERCIA * self.vy + random.randint(1)*(self.py - self.y) + random.randint(1)*(Particle.g_best_y - self.y)
    #actualiza velocidad (fórmula mezclada)
    #vx = w * vx + random(0,1)*C1*(px - x) + random(0,1)*C2*(gbestx - x)
    #vy = w * vy + random(0,1)*C1*(py - y) + random(0,1)*C2*(gbesty - y)
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
  
  # ------------------------------ despliega partícula
  # void display(){
  #   color c=surf.get(int(x),int(y)) 
  #   fill(c)
  #   ellipse (x,y,d,d)
  #   # dibuja vector
  #   stroke(#ff0000)
  #   line(x,y,x-10*vx,y-10*vy)
  # }
 #fin de la definición de la clase Particle