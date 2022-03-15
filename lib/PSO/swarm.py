import sys, numpy as np
from lib.PSO.particle import *


class Swarm:
    def __init__(self, dimension: int, population: int, floor, ceiling):
        self.particles = [Particle(dimension, floor, ceiling) for i in range(population)]
        self.__generation = 1
        self.__population = population
        self.gbest_index = 0
        self.gbest = self.particles[0]
        self.xs = []
        self.foms = []
        self.p_xs = []
        self.p_foms = []


    def get_particle(self, i: int):
        """
        particle NO: 1 ~ population
        :return: particle
        """
        return self.particles[i-1]

    def get_particles(self):
        """
        :return: list contain dimension particles
        """
        return self.particles

    def update_fom(self, fom: list):
        """
        update p/g best by fom calculated outside,
        this function will make all particle ready to do evolution
        :return boolean list, true if pbest changed
        """
        pbest_changed = []
        for i in range(self.__population):
            self.particles[i].set_fom(fom[i])
            pbest_changed.append(self.particles[i].update_pbest())
            if fom[i] > self.gbest.get_best_fom():
                self.gbest_index = i
                self.gbest = self.particles[i]

        self.xs = []
        self.foms = fom
        self.p_xs = []
        self.p_foms = []
        for particle in self.particles:
            self.xs.append(particle.get_x())
            self.p_xs.append(particle.get_pbest())
            self.p_foms.append(particle.get_best_fom())
        return pbest_changed

    def evolution(self):
        for particle in self.particles:
            particle.evolution(self.gbest)
        self.__generation = self.__generation + 1

    def discrete(self, para_no: int, precisions):
        # used to discrete specific parameter
        for particle in self.particles:
            particle.discrete(para_no, precisions)






