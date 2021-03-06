'''This file groups the 6 asked methods and some useful additionnal others'''

import numpy as np
from helpers import *


'''------------ 6 Required Methods ------------'''

#Linear regression using gradient descent
def least_squares_GD(y, tx, initial_w, max_iters, gamma):
    w = initial_w
    for n_iter in range(max_iters):
        gradient = compute_gradient(y, tx, w)
        loss = compute_mse(y, tx, w)
        w = w - gamma * gradient
    return w, loss


#Linear regression using stochastic gradient descent
def least_squares_SGD(y, tx, initial_w, max_iters, gamma):
    batch_size = 1
    w = initial_w
    loss = 0
    for batch_y, batch_x in batch_iter(y, tx, batch_size, num_batches=max_iters):
        gradient = compute_gradient(batch_y, batch_x, w)
        loss = compute_mse(y, tx, w)
        w = w - gamma * gradient          
    return w, loss


#Least squares regression using normal equations
def least_squares(y, tx):
    w = np.linalg.solve(np.dot(tx.transpose(),tx), np.dot(tx.transpose(), y))
    loss = compute_mse(y, tx, w)
    return w, loss


#Ridge regression using normal equations
def ridge_regression(y, tx, lambda_):
    temp = np.dot(tx.transpose(), tx) + (lambda_* 2 * tx.shape[0]) * np.identity(tx.shape[1])
    w = np.linalg.solve(temp, np.dot(tx.transpose(), y))
    loss = compute_mse(y,tx,w)
    return w, loss


#Logistic regression using gradient descent
def logistic_regression(y, tx, initial_w, max_iters, gamma):
    threshold = 1e-8
    losses = []
    w = initial_w
    for iter in range(max_iters):
        loss, w = learning_by_gradient_descent(y, tx, w, gamma)
        # converge criterion
        losses.append(loss)
        if len(losses) > 1 and np.abs(losses[-1] - losses[-2]) < threshold:
            break
    return w, losses[-1]

        
#Regularized logistic regression using gradient descent
def reg_logistic_regression(y, tx, lambda_, initial_w, max_iters, gamma):
    threshold = 1e-8
    losses = []
    w = initial_w
    for iter in range(max_iters):
        # get loss and update w.
        loss, w = learning_by_penalized_gradient(y, tx, lambda_, w, gamma)
        # converge criterion
        losses.append(loss)
        if len(losses) > 1 and np.abs(losses[-1] - losses[-2]) < threshold:
            break
    return w, losses[-1]



'''------------ Other Additionnal Methods ------------'''

#Compute error of the model
def compute_loss(y, tx, w):
    e = y - np.dot(tx,w)
    return e

#Compute MSE using loss function
def compute_mse(y, tx, w):
    e = compute_loss(y, tx, w)
    return 1/(2*tx.shape[0]) * np.dot(np.transpose(e),e)

#Compute the RMSE using MSE
def compute_rmse(y, tx, w):
    return np.sqrt(2 * compute_mse(y, tx, w))

#Compute the gradient for the gradient descent
def compute_gradient(y, tx, w):
    e = y - np.dot(tx,w)
    gradient = -1/tx.shape[0] * np.dot(np.transpose(tx),e)
    return gradient

#Compute sigmoid function for a scalar
def sigmoid_scalar(t):
    if t > 0:
        return 1 / (1 + np.exp(-t))
    return np.exp(t) / (1 + np.exp(t))

#Sigmoid function for matrix
sigmoid = np.vectorize(sigmoid_scalar)

#Compute loss for logistic regression
def calculate_loss(y, tx, w):
    return np.sum(np.log(1 + np.exp(tx.dot(w))) - y.transpose().dot(tx.dot(w)))

#Compute gradient for logistic regression
def calculate_gradient(y, tx, w):
    temp = sigmoid(tx.dot(w)) - y
    return tx.transpose().dot(temp)

#Compute Hessian matrix for logistic regression
def calculate_hessian(y, tx, w):
    S = sigmoid(tx.dot(w)) * (1 - sigmoid(tx.dot(w)))
    S = np.diag(np.ravel(S))
    return tx.transpose().dot(S).dot(tx)

#One step of Newton's method
def learning_by_newton_method(y, tx, w, gamma):
    loss = calculate_loss(y, tx, w)
    gradient = calculate_gradient(y, tx, w)
    hessian = calculate_hessian(y, tx, w)
    w = w - gamma * np.linalg.inv(hessian).dot(gradient)
    return loss, w

#One step of gradient descent using logistic regression
def learning_by_gradient_descent(y, tx, w, gamma):
    loss = calculate_loss(y, tx, w)
    gradient = calculate_gradient(y, tx, w)
    w = w - gamma * gradient
    return loss, w

#Compute loss, gradient, hessian for regularized logistic regression
def penalized_logistic_regression(y, tx, w, lambda_):
    loss = calculate_loss(y, tx, w) + lambda_ / 2 * np.linalg.norm(w)**2
    gradient = calculate_gradient(y, tx, w) + lambda_ * w * 2
    #hessian = calculate_hessian(y, tx, w) + np.diag(2 * lambda_ * np.ones(calculate_hessian(y, tx, w).shape[0]))
    return loss, gradient

#One step of gradient descent using regularized logistic regression
def learning_by_penalized_gradient(y, tx, lambda_, w, gamma ):
    loss, gradient = penalized_logistic_regression(y, tx, w, lambda_)
    w = w - gamma * gradient
    return loss, w

