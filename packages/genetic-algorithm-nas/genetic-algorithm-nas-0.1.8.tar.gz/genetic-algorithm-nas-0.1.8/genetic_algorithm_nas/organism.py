import numpy as np 
import random 
from tensorflow.keras.layers import Input, Add, Conv2D, BatchNormalization, GlobalAveragePooling2D, Dense
from tensorflow.keras import Model 
import tensorflow.keras as keras 
import tensorflow as tf 
from .errors import *

class Organism: 
    """
        Organism, is a whole component which includes multiple chromosome, in our case it is one chromosome.
        Attributes:
            params            : HyperParameter Dictionary, that will be used to build a chromosome.
            prev_phase_best   : It is the previous phase best organism object. Best One decided based on fitness score.
            phase             : Phase Number.
    """
    def __init__(self, params, prev_phase_best=None, phase=0): 
        self.params = params 
        self.prev_phase_best = prev_phase_best
        self.phase = phase
        self.chromosome = None
        self.model = None

        if phase != 0:
            self.last_model = prev_phase_best.model

    def build_model(self):
        """
            This method, will build a tensorflow model, by using the hyperparameter and layer details of the self.chromosome. It has
            different structure for phase0 and rest of other phases.
        """
        try: 
            keras.backend.clear_session()
            inputs = Input(shape=(32,32,3))
            if self.phase != 0:
                intermediate_model = Model(inputs=self.last_model.input,
                                           outputs=self.last_model.layers[-3].output)
                for layer in intermediate_model.layers:
                    layer.trainable = False
                inter_inputs = intermediate_model(inputs)
                x = Conv2D(filters=self.chromosome['a_output_channels'],
                           padding='same',
                           kernel_size=self.chromosome['a_filter_size'],
                           use_bias=self.chromosome['a_include_BN'])(inter_inputs)

                self.chromosome['activation_type'] = self.prev_phase_best.chromosome['activation_type']
            else:

                x = Conv2D(filters=self.chromosome['a_output_channels'],
                           padding='same',
                           kernel_size=self.chromosome['a_filter_size'],
                           use_bias=self.chromosome['a_include_BN'])(inputs)
            if self.chromosome['a_include_BN']:
                x = BatchNormalization()(x)
            x = self.chromosome['activation_type']()(x)
            if self.chromosome['include_pool']:
                x = self.chromosome['pool_type'](strides=(1,1),
                                                 padding='same')(x)
            if self.phase != 0 and self.chromosome['include_layer'] == False:

                if self.chromosome['include_skip']:
                    y = Conv2D(filters=self.chromosome['a_output_channels'],
                               kernel_size=(1,1),
                               padding='same')(inter_inputs)
                    x = Add()([y,x])
                x = GlobalAveragePooling2D()(x)
                x = Dense(10, activation='softmax')(x)
            else:

                x = Conv2D(filters=self.chromosome['b_output_channels'],
                           padding='same',
                           kernel_size=self.chromosome['b_filter_size'],
                           use_bias=self.chromosome['b_include_BN'])(x)
                if self.chromosome['b_include_BN']:
                    x = BatchNormalization()(x)
                x = self.chromosome['activation_type']()(x)
                if self.chromosome['include_skip']:
                    y = Conv2D(filters=self.chromosome['b_output_channels'],
                               padding='same',
                               kernel_size=(1,1))(inputs)
                    x = Add()([y,x])
                x = GlobalAveragePooling2D()(x)
                x = Dense(10, activation='softmax')(x)
            model = Model(inputs=[inputs], outputs=[x])
            model.compile(optimizer='adam',
                               loss='categorical_crossentropy',
                               metrics=['accuracy']) 
            self.model = model
        
        except Exception as error:
            return error

    def build_chromosome(self): 
        """
            This Method will build a chromosome, by combining a genes(different hyperparameter values). Once it build a chromosome,
            with random hyperparameter values, it will assign the chromosome dictionary to the property(self.chromosome). Phase0, has 
            different chromosome that reset other phases.
        """
        try: 
            if self.phase == 0:
                phase_params = self.params["phase0"]
                self.chromosome = {
                    'a_filter_size': random.choice(phase_params['a_filter_size']),
                    'a_include_BN' : random.choice(phase_params['a_include_BN']),
                    'a_output_channels' : random.choice(phase_params['a_output_channels']),
                    'activation_type' : random.choice(phase_params['activation_type']),
                    'b_filter_size' : random.choice(phase_params['b_filter_size']),
                    'b_include_BN' : random.choice(phase_params['b_include_BN']),
                    'b_output_channels' : random.choice(phase_params['b_output_channels']),
                    'include_pool' : random.choice(phase_params['include_pool']),
                    'pool_type' : random.choice(phase_params['pool_type']),
                    'include_skip' : random.choice(phase_params['include_skip']),
                }

            else: 
                phase_params = self.params["rest_phases"]
                self.chromosome = {
                    'a_filter_size': random.choice(phase_params['a_filter_size']),
                    'a_include_BN' : random.choice(phase_params['a_include_BN']),
                    'a_output_channels' : random.choice(phase_params['a_output_channels']),
                    'include_layer' : random.choice(phase_params['include_layer']),
                    'b_filter_size' : random.choice(phase_params['b_filter_size']),
                    'b_include_BN' : random.choice(phase_params['b_include_BN']),
                    'b_output_channels' : random.choice(phase_params['b_output_channels']),
                    'include_pool' : random.choice(phase_params['include_pool']),
                    'pool_type' : random.choice(phase_params['pool_type']),
                    'include_skip' : random.choice(phase_params['include_skip']),
                }
        
        except Exception as error:
            return error
