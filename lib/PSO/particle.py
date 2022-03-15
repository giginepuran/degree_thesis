import math
import numpy as np
import random
from PSO.particle import *


class Particle:
    def __init__(self, dimension: int, floor: float, ceiling: float):
        # give particle a random vector (dimension, 1)
        self._x = np.random.rand(dimension, 1)
        if isinstance(floor, (float, int)) and isinstance(ceiling, (float, int)):
            self.__floor = np.array([floor for i in range(dimension)]).reshape(dimension, 1)
            self.__ceiling = np.array([ceiling for i in range(dimension)]).reshape(dimension, 1)
        elif isinstance(floor, list) and isinstance(ceiling, list):
            self.__floor = np.array(floor).reshape(dimension, 1)
            self.__ceiling = np.array(ceiling).reshape(dimension, 1)
        self._x = self._x * (self.__ceiling - self.__floor) + self.__floor
        # index of cognitive best
        self._pbest = self._x
        self._bestFOM = -math.inf
        self._FOM = -math.inf
        self._inertia = np.array([0 for i in range(dimension)]).reshape(dimension, 1)

    # evolution by another particle(gbest)
    def evolution(self, gbest):
        """
        Coefficients of the update equation are choose from
        Daniel Bratton, Defining a Standard for Particle Swarm Optimization (2007) p.3

        :param gbest: global best Particle from swarm
        :return: null
        """
        velocity = (0.72984 * self._inertia +
                    1.496172 * random.random() * (self._pbest - self._x) +
                    1.496172 * random.random() * (gbest.get_pbest() - self._x))
        new_x = self._x + velocity
        # ensure particle inside boundary
        new_x = np.where(new_x > self.__floor, new_x, self.__floor)
        new_x = np.where(new_x < self.__ceiling, new_x, self.__ceiling)
        self._inertia = new_x - self._x
        self._x = new_x

    def update_pbest(self):
        if self._FOM > self._bestFOM:
            self._pbest = self._x
            self._bestFOM = self._FOM
            return True
        return False

    def get_pbest(self):
        """
        :return: ndarray
        """
        return self._pbest.copy()

    def get_x(self):
        """
        :return: ndarray
        """
        return self._x.copy()

    def get_best_fom(self):
        """
        :return: float
        """
        return self._bestFOM

    def set_fom(self, fom):
        self._FOM = fom

    def get_fom(self):
        return self._FOM

    def discrete(self, para_no: int, precisions):
        self._x[para_no-1][0] = round(self._x[para_no-1][0] / precisions, 0) * precisions


