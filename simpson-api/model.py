import cv2
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten


def create(input_shape, num_classes):
    """
    This model architecture and code was copied from a Kaggle submission here:
    https://www.kaggle.com/alexattia/visualizing-predicted-characters

    It is a CNN Keras model with 6 convolutions.
    :param input_shape: input shape, generally X_train.shape[1:]
    :return: Keras model, RMS prop optimizer
    """
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(256, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(256, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    return model


class SimpsonClassifier(object):

    def __init__(self, weights_path, pic_size=64):

        self.weights_path = weights_path
        self.input_shape = (pic_size, pic_size, 3)
        self.map_characters = {0: 'Abraham Simpson',
                               1: 'Apu Nahasapeemapetilon',
                               2: 'Bart Simpson',
                               3: 'Charles Montgomery Burns',
                               4: 'Chief Wiggum',
                               5: 'Comic Book Guy',
                               6: 'Edna Krabappel',
                               7: 'Homer Simpson',
                               8: 'Kent Brockman',
                               9: 'Krusty the Clown',
                               10: 'Lisa Simpson',
                               11: 'Marge Simpson',
                               12: 'Milhouse Van Houten',
                               13: 'Moe Szyslak',
                               14: 'Ned Flanders',
                               15: 'Nelson Muntz',
                               16: 'Principal Skinner',
                               17: 'Sideshow Bob'}

        self.num_classes = len(self.map_characters)

        # Load model
        self.model = create(self.input_shape, self.num_classes)
        self.model.load_weights(weights_path)

    def run(self, img):
        '''
        Run the model on the input image. Return the prediction and probability
        in a dictionary
        '''
        y_pred = self.model.predict_classes(img)[0]
        y_pred_name = self.map_characters[y_pred]
        y_prob = round(self.model.predict_proba(img)[0][y_pred], 2)
        return {'y_pred': y_pred_name, 'y_prob': str(y_prob)}
