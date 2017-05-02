import time
import os
import sys
import math
import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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

    def __init__(self, P, N, H, E, T):
        #self.q = 1.60218 * (10**(-19))
        #self.alpha = (q * E * H)/(k * T * N)
        k = 1.38065 * (10**(-23))
        self.P = P
        self.N = N
        self.kT = k * T
        self.delta = float((H / N) * E)

    def jump(self, particle):
        # Determine if the particle will go up or down:
        div = 1 / (self.P + 1)
        random.seed()
        rand = random.random()
        if (rand < div) & (particle.state != 0):
            particle.state -= 1

        else:
            try:
                prob = math.exp(-self.delta / self.kT)
            except OverflowError:
                sys.exit("Probability too low.")
            rand = random.random()
            if (rand < prob) & (particle.state != self.N):
                particle.state += 1

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

    P = float(raw_input("P: "))
    T = float(raw_input("T: "))
    #N = int(raw_input("N: "))
    #H = float(raw_input("H: "))
    #E = float(raw_input("E: "))

    N = 30
    H = 1 * (10**(-9))
    E = 3 * (10**(-10))

    world = World(P, N, H, E, T)
    for i in range(30):
        particle = Particle(N / 2)
    for i in range(75):
        world.rep()
        world.step()


    # plt.hist(pi.limits, pi.errors, 'go', linestyle='None')
    # plt.ylabel('Accuracy')
    # plt.xlabel('Number of Terms')
    # plt.title('Monte Carlo')
    # plt.grid(True)
    # plt.errorbar(pi.limits, pi.errors, yerr=pi.sigmas, linestyle='None')
    # plt.show()
