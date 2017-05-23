import time
import os
import sys
import math
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


#------- Glogal "Constants" -------#
K_B = 8.61733 * (10**(-5)) # eV / K
TEMP = 300 # K
DEGENERACY = 10
LEVELS = 7
START_LEVEL = 10**(18)
FREQUENCY = 10**(-12) # 1/sec

DOWN_PROB = 0.5
NUM_PARTS = 10**(2)
NUM_STEPS = 10**(2)
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

    def __init__(self, P, T, delta):
        self.deltaE = delta
        # compute energy of the whole ladder
        self.gap = self.deltaE * LEVELS
        self.energy = 0
        self.N = LEVELS
        self.P = P
        self.kT = K_B * T
        try:
            alpha = self.deltaE / self.kT
        except OverflowError:
            sys.exit("Error creating alpha.")
        lnp = np.log(self.P)
        self.div = 1 / (np.exp(2*(lnp - alpha)) + 1)

    def jump(self, particle):
        random.seed()
        rand = random.random()
        # Test if particle will go down
        if (rand < self.div) & (particle.state != 0):
            particle.state -= 1
        # If not it goes up or...
        elif (self.div < rand) & (particle.state != self.N):
            particle.state += 1
        # Jumps down. Add this energy to cumulative energy
        elif (particle.state == self.N) & (rand < DOWN_PROB):
            particle.state = 0
            self.energy += self.gap

    def power(self):
        time = FREQUENCY * NUM_STEPS
        # Convert eV to Joules
        energy = self.energy * (1.6022*(10**(-19)))
        power = energy / time
        # Compute the power in kW per cubic centimeter
        particle_diff = START_LEVEL / NUM_PARTS
        self.kW = (power * particle_diff) / 1000
        return self.kW

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

    # Make particles at initial energy 0
    for i in xrange(NUM_PARTS):
        particle = Particle(0)

    # Determine equilibrium sized gap
    equ_gap = K_B * TEMP * np.log(DEGENERACY)
    # Setup lists to be plotted
    gaps = np.linspace(0, equ_gap, 100)
    powers = []

    for gap in gaps:
        world = World(DEGENERACY, TEMP, gap)
        for particle in Particle:
            particle.state = 0
        for i in range(NUM_STEPS):
            world.step()
        powers.append(world.power())

    plt.plot(gaps, powers, 'g')
    plt.ylabel('Power (kW / cc)')
    plt.xlabel('Energy Gap (eV)')
    # plt.ylim([0, 1])
    # plt.ylim([0, .01])
    plt.title('T=300 Degeneracy=10 N=2')
    plt.grid(True)
    plt.savefig("power.png")
