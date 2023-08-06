import logging
from tensorflow import keras
from tensorflow.keras.layers import Layer


class MCDropout(keras.layers.Dropout):
    def call(self, inputs):
        return super().call(inputs, training=True)


class MCSpatialDropout1D(keras.layers.SpatialDropout1D):
    def call(self, inputs):
        return super().call(inputs, training=True)


class DropoutLayer(Layer):
    """
    This class creates a Droupout layer for a model.
    """
    def __init__(self, drp_rate=0.1, spatial=True):
        super(DropoutLayer, self).__init__()
        self.drp_rate = drp_rate
        self.spatial = spatial
        if spatial is True:
            self.drp = MCSpatialDropout1D(drp_rate)
        else:
            self.drp = MCDropout(drp_rate)

    def call(self, inputs):
        return self.drp(inputs)
