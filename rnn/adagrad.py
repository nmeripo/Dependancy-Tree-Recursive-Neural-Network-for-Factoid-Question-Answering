import numpy as np

class Adagrad():
    def __init__(self, dim):
        self.dim = dim

	# smoothing term to avoid 0 division
        self.eps = 1e-3

        # initial learning rate
        self.learning_late = 0.05

        # stores sum of squared gradients
        self.h = np.zeros(self.dim)

    def rescale_update(self, gradient):
        curr_rate = np.zeros(self.h.shape)
        self.h += gradient ** 2
	# the square root operation in the denominatior turns out to be very important and without it the algorithm performs much worse
        curr_rate = self.learning_late / np.sqrt(self.h) + self.eps
        return curr_rate * gradient

    def reset_weights(self):
        self.h = np.zeros(self.dim)
