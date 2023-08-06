import random
import numpy as np 
from typing import *
import tensorflow as tf 
from .errors import *
from .organism import *

class GenPopulation:
    def __init__(self): 
        self.population = []

    def generate(self, params: dict, n_population: int, prev_phase_best: Organism, phase_no: int) -> List: 
        """
            Params: 
                number_of_features: is used to encode the actual data into genotype.
                max_pop_size:       is used to restrict number of individual generation.
                max_featrures:      how many features needed to be in the subset. 
                                      if max_features is 0, then maximum subset size is number of number 
        """
        try: 
            self.population = []
            for individual in range(n_population):
                _organism = Organism(
                    params = params,
                    prev_phase_best = prev_phase_best,
                    phase = phase_no
                )
                _organism.build_chromosome()
                _organism.build_model()
                self.population.append(_organism)

            return np.array(self.population)
        
        except Exception as error:
            return error
