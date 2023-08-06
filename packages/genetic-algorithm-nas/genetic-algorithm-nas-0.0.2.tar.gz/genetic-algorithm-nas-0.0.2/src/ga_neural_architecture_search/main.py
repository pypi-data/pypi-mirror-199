import errors import *
import tensorflow.keras as keras 
import tensorflow as tf 
import numpy as np 
from tensorflow.keras.layers import (Conv2D, BatchNormalization, MaxPool2D, ReLU,
                                                 ELU, LeakyReLU, Flatten, Dense, AveragePooling2D)

import tensorflow as tf 
import tensorflow.keras as keras 


class GeneticAlgorithm: 
    
    def __init__(self), X_train, y_train, X_test, y_test: 
        assert len(X_train) == len(y_train), "Number of datapoints in X_train and y_train, does'nt match"
        assert len(X_test) == len(y_test), "Number of datapoints in X_test and y_test, does'nt match"
        self.X_train = X_train 
        self.y_train = y_train 
        self.X_test = X_test
        self.y_test = y_test
        self.mutation_rate = 0.1
        self.survival_rate = 0.60
    
    def evolve(num_phase: int, num_generation: int, num_population: int, params: dict, verbose=True): 
        """
            - This function contains all the component of Variable Length Genetic Algorithm. It starts generating the 
                initial population, and for that population fitness score will be computed, from that population, some of the 
                individuals will be survived to mate and it will put into the mating pool, from which the next generation population
                will be generation by doing reproduction(mating), the individuals from the mating pool randomly picked mated with each
                other. Some of the parent will be mutated before it is used for the reproduction.
            - Params:
                num_phase        : phase, directly proportional to number of layers(conv2d). 
                num_generation   : how many generation do we need to evolve our initial pop in each phase.
                num_population   : size of the population.
                params         : Dictionary, where key is hyperparameter, value is value of hyperparameter 
        """
        assert num_population % 2 == 0, "Input value for number of population, should be even."
        assert num_generation > 1, "Number of generation should be greater than 1"
        assert type(num_phase) == int, "Type Error: Int is required"
        assert type(num_generation) == int, "Type Error: Int is required"
        assert type(num_population) == int, "Type Error: Int is required"
        assert type(params) == dict, "Type Error: Dict is required"
        assert type(verbose) == bool, "Type Error: Bool is required"
        assert params.get("phase0", False) != False, "Params dictionary, need a key name as phase0"
        assert params.get("rest_phases", False) != False, "Params dictionary, need a key name as rest_phases"

        try: 
            prev_phase_best = None 
            population = []
            generator = GenPopulation()
            fitness_function = FitnessFunction()

            train_ds, test_ds, test_X, test_y = preprocess_data((self.X_train, self.y_train), (self.X_test, self.y_test))
            for phase in range(num_phase): 
                print(f"phase: {phase}")
                population = generator.generate(
                    params, 
                    num_population,
                    prev_phase_best,
                    phase
                )
                for generation in range(num_generation):         
                    print(f"    Generation: {generation}") if verbose else None

                    fitness_scores, prediction_scores = fitness_function.get_fitness_score(population, train_ds, 
                                                                                                   test_ds, test_X, test_y)
                    print("prediction scores: ", prediction_scores) if verbose else None

                    if len(population) != len(fitness_scores):
                        raise LengthError("Length of Fitness Scores and Population array does'nt match")

                    num_mating_pool_individuals = int(self.survival_rate * num_population)

                    mating_pool_pop  = []
                    mating_pool_fitness_scores = []

                    fs_copy = fitness_scores.copy()
                    pop_copy = population.copy()

                    for _ in range(num_mating_pool_individuals): 
                        index_val = fs_copy.argmax()
                        mating_pool_pop.append(pop_copy[index_val])
                        mating_pool_fitness_scores.append(fs_copy[index_val])
                        np.delete(fs_copy, index_val)
                        np.delete(pop_copy, index_val)

                    del pop_copy
                    del fs_copy
                    if phase == 0: 
                        param = params.get("phase0")
                    else: 
                        param = params.get("rest_phases")

                    mating_pool_fitness_scores = np.array(mating_pool_fitness_scores)
                    next_gen_population = get_next_generation_population(mating_pool_pop, mating_pool_fitness_scores,
                                                                                            self.mutation_rate, param, num_population)
                    population = next_gen_population

                prev_phase_best_index = fitness_scores.argmax()
                prev_phase_best = population[prev_phase_best_index]

            return population, fitness_scores, prev_phase_best, prediction_scores

        except LengthError as error:
            return error 

