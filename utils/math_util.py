import numpy as np

# Activations and their derivatives

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def relu(x):
    return x * (x > 0)


def relu_derivative(x):
    return x > 0

def tanh_derivative(x):
    return 1 - np.square(x)


def norm_tanh_derivative(x):
    norm = np.linalg.norm(x)
    y = x - np.power(x, 3)
    dia = np.diag((1 - np.square(x)).flatten()) / norm
    pro = y.dot(x.T) / np.power(norm, 3)
    out = dia - pro
    return out

# Cost Functions

def crossent(label, classification):
    return -np.sum(label * np.log(classification))


def crossent_loss(label, classification):
    return classification - label


def square_loss(label, classification):
    err = label - classification
    return 0.5 * err.T.dot(err)
