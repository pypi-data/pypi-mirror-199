import random 
import numpy as np 
from errors import *

def pick_parents(population, fitness_score): 
    """
        This function, will pick two parent chromosomes from the population.
        Params:
            population      : Array of individuals created from GenPopulation Class.
            fitness_score   : Score calculated for each individual in the population by the fitness class.
    """
    try: 
        parent_1, parent_2 = random.choices(population, fitness_score, k=2)
        return parent_1, parent_2
    
    except Exception as error:
        return error
    
    
def reproduce(parent_1, parent_2):
    """
        This function will generate a new childrens by combining two parents gene.
        Params:
            parent_1       : parent_1 array that is picked by the pick_parent function.
            parent_2       : parent_2 array that is picked by the pick_parent function.
    """
    try:
        child1_chromosome, child2_chromosome = {}, {}
        parent_1_chromosome = parent_1.chromosome
        parent_2_chromosome = parent_2.chromosome
        parent_1_chromosome_length = len(parent_1_chromosome)    
        chromosome_breakage_point = random.randint(1, parent_1_chromosome_length-1) 
        
        if chromosome_breakage_point > parent_1_chromosome_length: 
            raise ValueError("chromosome breakage point value is greater than the chromosome dictionary")

        for i, key in enumerate(parent_1_chromosome): 
            if i <= chromosome_breakage_point: 
                child1_chromosome[key] = parent_1_chromosome[key]

        for i, key in enumerate(parent_2_chromosome): 
            if i <= chromosome_breakage_point: 
                child2_chromosome[key] = parent_2_chromosome[key]

        for i, key in enumerate(parent_2_chromosome): 
            if i > chromosome_breakage_point: 
                child1_chromosome[key] = parent_2_chromosome[key]

        for i, key in enumerate(parent_1_chromosome):       
            if i > chromosome_breakage_point: 
                child2_chromosome[key] = parent_1_chromosome[key]
        return child1_chromosome, child2_chromosome
    
    except ValueError as error:
        return error

