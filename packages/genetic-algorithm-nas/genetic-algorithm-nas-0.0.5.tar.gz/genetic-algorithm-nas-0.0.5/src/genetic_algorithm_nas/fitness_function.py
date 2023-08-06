import random 
import numpy as np 
from tensorflow.keras.optimizers import Adam
import tensorflow as tf 
import math 
import tensorflow.keras as tf 
from sklearn.metrics import accuracy_score
from errors import *

class FitnessFunction: 
    def __init__(self): 
        '''
            Params:
                population: Population array from generate_pop method.
                model: Model from build model method.
                train_X, train_y: training data for our model.
                test_X, test_y: testing data for our model.
                scoring_criteria: On what basis scoring, needs to happend eg: Accuracy, f1-score, recall, precision.
        '''
        self.scores = []

    def train_model(self, individual, train_ds):
        """
            This method, will train a neural net model, with the specific individual.
            Params:
                train_X       : Independent variable to the model.
                train_y       : Dependent variable to the model.
                input_dims    : Input dimension of the model, len(individual).
        """
        try: 
            individual.fit(train_ds, epochs=1,
                                   verbose=0, batch_size = 64)
            return individual
        
        except Exception as error:
            return error

    def test_model(self, individual, test_ds, test_X): 
        """
            This method, will return a prediction for the prediction data.
            Params:
                test_X        : Independent Variable of testing data.
                model         : fitted model returned by the train_model method.
                train_X       : Independent Variable of training data.
        """
        try: 
            prediction_score = individual.evaluate(test_ds, 
                                                       verbose=0, batch_size=64)
            pred_y = individual.predict(test_X, batch_size=64, verbose=0)
            return prediction_score, pred_y
        
        except Exception as error:
            return error
        
    def get_prediction_score(self, model, test_ds, test_X, test_y, prediction_score=True): 
        """
            This method, will calculate the metrics value for the prediction done by the model.
            Params: 
                y_true        : Ground Truth value of the testing data.
                y_pred        : Prediction data of the model.
                regression    : To specify, whether it is regression task or classfication task.
        """
        try: 
            if prediction_score: 
                score, y_pred = self.test_model(model, test_ds, test_X)
                test_y = test_y.numpy()
                test_y = [each.argmax() for each in test_y]
                y_pred = [each.argmax() for each in y_pred]
                return accuracy_score(test_y, y_pred)

            results = get_metrics_value(y_true, y_pred, regression)

            if not regression:
                acc, precision, recall, f1_score = results 

            else: rmse, adj_r2 = results

            if self.scoring_criteria == "rmse" and regression: 
                return ((0.9 * rmse) + (0.10 * adj_r2) )

            if self.scoring_criteria == "adj_r2" and regression: 
                return ((0.9 * adj_r2) + (0.1 * rmse))

            if self.scoring_criteria == "acc": 
                return ((0.88 * acc) + (0.03 * recall) + (0.03 * precision) + (0.03 * f1_score))

            if self.scoring_criteria == "recall": 
                return ((0.03 * acc) + (0.88 * recall) + (0.03 * precision) + (0.03 * f1_score))

            if self.scoring_criteria == "precision": 
                return ((0.03 * acc) + (0.03 * recall) + (0.88 * precision) + (0.03 * f1_score))

            if self.scoring_criteria == "f1": 
                return ((0.03 * acc) + (0.03 * recall) + (0.03 * precision) + (0.88 * f1_score))
        
        except Exception as error:
            return error

    def get_fitness_score(self, population, train_ds, test_ds, test_X, test_y): 
        try: 
            fitness_scores = []
            """
                This method calculates the fitness score.
                Params:
                    regression       : To specify, whether it is regression task or classfi
                    cation task.
            """
            for index, individual in enumerate(population): 
                model = individual.model
                trained_model = self.train_model(model, train_ds)
                model_pred_score = self.get_prediction_score(trained_model, test_ds, test_X, test_y, True)
                fitness_scores.append(model_pred_score)
                print(f"      Successfully calculated the fitness score for individual: {index}")

            fitness_scores = np.array(fitness_scores)
            return np.array(fitness_scores / sum(fitness_scores)), fitness_scores
        
        except Exception as error:
            return error 
