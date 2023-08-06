import tensorflow as tf 
import tensorflow.keras as keras 
import numpy as np
from .errors import *


def preprocess_data(training_data, testing_data): 
    """
        This Function used to convert the tensorflow data object into tensorflow eager object.
        Params: 
            training_data    : training data of the dataset.
            testing_data     : testing data of the dataset.
    """
    try: 
        (X_train, y_train), (X_test, y_test) = training_data, testing_data

        X_train = X_train.astype('float32')
        X_train = X_train/255.

        X_test = X_test.astype('float32')
        X_test = X_test/255.

        y_train = tf.reshape(tf.one_hot(y_train, 10), shape=(-1, 10))
        y_test = tf.reshape(tf.one_hot(y_test, 10), shape=(-1, 10))

        BATCH_SIZE = 256
        AUTOTUNE = tf.data.experimental.AUTOTUNE

        train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train))
        train_ds = train_ds.shuffle(1024).cache().batch(BATCH_SIZE).prefetch(AUTOTUNE)

        test_ds = tf.data.Dataset.from_tensor_slices((X_test, y_test))
        test_ds = test_ds.cache().batch(BATCH_SIZE).prefetch(AUTOTUNE)

        return train_ds, test_ds, X_test, y_test
    
    except Exception as error:
        return error
