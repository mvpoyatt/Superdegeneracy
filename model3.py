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
EQU_T = 1000
EQU_P = 3
LEVELS = 35
NUM_PARTS = 60
NUM_STEPS = 100
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
        #elif (particle.state == self.N):
        #    particle.state = 0

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
    for i in range(NUM_PARTS):
        particle = Particle(LEVELS / 2)
    for i in range(NUM_STEPS):
        world.rep()
        world.step()
        # if (i == 10) | (i == 40):
        #     time.sleep(1)


    # plt.hist(pi.limits, pi.errors, 'go', linestyle='None')
    # plt.ylabel('Accuracy')
    # plt.xlabel('Number of Terms')
    # plt.title('Monte Carlo')
    # plt.grid(True)
    # plt.errorbar(pi.limits, pi.errors, yerr=pi.sigmas, linestyle='None')
    # plt.show()
