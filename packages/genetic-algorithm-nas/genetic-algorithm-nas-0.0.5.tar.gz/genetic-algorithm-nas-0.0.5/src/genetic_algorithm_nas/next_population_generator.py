from errors import *    
from mutation import * 
from crossover import * 
import random 
import numpy as np 

def get_next_generation_population(population, fitness_score, mutation_rate, param, n_population): 
    """
        This function used to generate a new individauls by combining genes of the parensts from old population.
        Params:
            population      : Array of individuals created from GenPopulation Class.
            fitness_score   : Score calculated for each individual in the population by the fitness class.
            mutation_rate   : Amount of mutation needed to be done.
            param           : Hyperparameter dictionary, that will be used by the mutate function.
    """
    try: 
        new_generation_population = []
        n_individual_for_next_gen = int(n_population * 0.20)
        fs_copy = fitness_score.copy()
        pop_copy = population.copy()    
        for _ in range(n_individual_for_next_gen): 
            index_val = fs_copy.argmax()
            new_generation_population.append(pop_copy[index_val])
            np.delete(fs_copy, index_val)
            np.delete(pop_copy, index_val)
        
        del fs_copy
        del pop_copy
        
        n_iter = int(n_population//2 - (n_individual_for_next_gen / 2))
        print(n_iter, len(new_generation_population), "n_iter")
        for _ in range(n_iter): 
            parent_1, parent_2 = pick_parents(population, fitness_score)
            # Mutation.
            if random.random() < mutation_rate: 
                parent_1 = mutate(parent_1, param)

            if random.random() < mutation_rate: 
                parent_2 = mutate(parent_2, param)

            # Mating.
            child1_chromosome, child2_chromosome = reproduce(parent_1, parent_2)

            # Creating new organsim for next generation.
            child1_organism = Organism(parent_1.params, parent_1.prev_phase_best, parent_1.phase)
            child1_organism.chromosome = child1_chromosome
            child1_organism.build_model()

            child2_organism = Organism(parent_1.params, parent_1.prev_phase_best, parent_1.phase)
            child2_organism.chromosome = child2_chromosome
            child2_organism.build_model()

            new_generation_population.append(child1_organism)
            new_generation_population.append(child2_organism)
        
        if len(new_generation_population) != n_population: 
            raise LengthError("Length of new_generation_population array is not same as population")
            
        print("[+] Successfully generated the next generation's population.")
        return new_generation_population
    
    except LengthError as error:
        return error
