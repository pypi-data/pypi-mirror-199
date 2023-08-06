import numpy as np
import logging
from tqdm import tqdm


class Perceptron:
  def __init__(self, eta, epochs):
    # Small weight initialisation
    self.weights = np.random.randn(3) * 1e-4
    logging.info(f"Weights before training : \n {self.weights}")
    self.eta = eta
    self.epochs = epochs

  def activationFunction(self, inputs, weights):
    # Activation function (z) (z = x*w .i.e. inputs*weights)
    z = np.dot(inputs, weights) #(z = x*w .i.e. inputs*weights)
    return np.where(z > 0, 1, 0) # if condition is True, it will give 1 else 0 

  def fit(self, X, y):
    self.X = X  # Predictors
    self.y = y  # Target

    # Concationation (np.c_) of all the Predictors with bias(-1)
    X_with_bias = np.c_[self.X, -np.ones((len(self.X), 1))]
    logging.info(f"X with Bias: \n {X_with_bias}")

    for epoch in  tqdm(range(self.epochs), total= self.epochs, desc = "Training the model"):
      logging.info("--"*15)
      logging.info(f"For epoch: {epoch}")
      logging.info("--"*15)
      
      # Forward Propagation
      y_hat = self.activationFunction(X_with_bias, self.weights)
      logging.info(f"Predicted value after forward pass: \n {y_hat}")
      self.error = self.y - y_hat
      logging.info(f"Error: \n{self.error}")
      self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error)
      logging.info(f"Updated weights after epochs: \n{epoch}/{self.epochs} : \n{self.weights}")      
      logging.info("-----"*10)


  def predict(self, X):
    X_with_bias = np.c_[X, -np.ones((len(X), 1))]
    return self.activationFunction(X_with_bias, self.weights)
  
  def total_loss(self):
    total_loss = np.sum(self.error)
    logging.info(f"Total loss: {total_loss}")
    return total_loss