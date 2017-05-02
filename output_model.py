import time
import os
import sys
import math
import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


#------- Glogal "Constants" -------#
EQU_T = 300 # K
EQU_P = 3
LEVELS = 5
NUM_PARTS = 10**(3)
NUM_STEPS = 100
DOWN_PROB = 0.5
FREQUENCY = 10**(-11) # 1/sec
#-------- End "Constants" ---------#


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class Particle:
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, start):
        self._registry.append(self)
        self.state = start


class World:

    def __init__(self, P, T):
        # self.k = 8.61733 * (10**(-5)) # eV / K
        self.k = 1.38065 * (10**(-23)) # J / K
        self.deltaE = self.k * EQU_T * np.log(EQU_P)
        # compute energy of the whole ladder
        self.gap = self.deltaE * LEVELS
        self.energy = 0
        self.N = LEVELS
        self.P = P
        self.kT = self.k * T

    def jump(self, particle):
        try:
            alpha = self.deltaE / self.kT
        except OverflowError:
            sys.exit("Error creating alpha.")
        lnp = np.log(self.P)
        div = 1 / (np.exp(2*(lnp - alpha)) + 1)
        random.seed()
        rand = random.random()
        # Test if particle will go down
        if (rand < div) & (particle.state != 0):
            particle.state -= 1
        # If not it goes up
        elif (div < rand) & (particle.state != self.N):
            particle.state += 1
        # Add energy released to world if particle jumps down
        elif (particle.state == self.N) & (rand < DOWN_PROB):
            particle.state = 0
            self.energy += self.gap

    def power(self):
        time = FREQUENCY * NUM_STEPS
        self.power = self.energy / time

    def rep(self):
        os.system('clear')
        states = [0] * (self.N + 1)
        for particle in Particle:
            states[particle.state] += 1
        for i in range(len(states)-1,-1,-1):
            print i, ": ",
            for j in range(states[i]):
                print "o",
            print ""
        time.sleep(.125)

    def step(self):
        for particle in Particle:
            self.jump(particle)
        


if __name__ == '__main__':

    P = float(raw_input("Degeneracy: "))
    T = float(raw_input("Temperature: "))

    world = World(P, T)
    for i in xrange(NUM_PARTS):
        particle = Particle(LEVELS / 2)
    for i in range(NUM_STEPS):
        # world.rep()
        world.step()
    world.power()
    print "Power: ", world.power, " W"



