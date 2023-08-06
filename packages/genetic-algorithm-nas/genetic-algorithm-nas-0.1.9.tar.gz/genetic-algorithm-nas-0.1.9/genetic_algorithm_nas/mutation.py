import random 
import numpy as np
from .errors import *

def mutate(individual, param):
    """
        This function is used to mutate the childrens based randomly.
        Params:
            mutation_rate     : It is probability value, that decides whether to mutate or not.
    """
    try: 
        individual_chromosome = individual.chromosome
        mutation_index = random.randint(0, len(individual_chromosome)-1)
        print(mutation_index > len(individual_chromosome), "mutate")
        if mutation_index > len(individual_chromosome): 
            raise ValueError("chromosome breakage point value is greater than the chromosome dictionary")
            
        for i, key in enumerate(individual_chromosome): 
            if i == mutation_index: 
                individual.chromosome[key] = random.choice(param[key])

        individual.chromosome = individual_chromosome
        return individual
    
    except ValueError as error:
        return error

