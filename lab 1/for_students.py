import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

data = get_data()
inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy().reshape(-1, 1)
x_train = train_data['Weight'].to_numpy().reshape(-1, 1)

y_test = test_data['MPG'].to_numpy().reshape(-1, 1)
x_test = test_data['Weight'].to_numpy().reshape(-1, 1)

# TODO: calculate closed-form solution
obs_matrix = np.hstack((np.ones(x_train.shape), x_train))
theta_best = np.linalg.inv(obs_matrix.T.dot(obs_matrix)).dot(obs_matrix.T).dot(y_train)

# TODO: calculate error
MSE = sum((y_test - (theta_best[0] + theta_best[1] * x_test)) ** 2) / len(x_test)
#print(y_test - (theta_best[0] + theta_best[1] * x_test))
print("test: MSE: ",MSE, ", theta: ", theta_best.flatten())

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0][0]) + float(theta_best[1][0]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# TODO: standardization
x_train_mean = np.mean(x_train, axis=0)[0]
x_train_standardization_deviation = np.std(x_train, axis=0)[0]
x_train = (x_train - x_train_mean) / x_train_standardization_deviation

y_train_mean = np.mean(y_train, axis=0)[0]
y_train_standardization_deviation = np.std(y_train, axis=0)[0]
y_train = (y_train - y_train_mean) / y_train_standardization_deviation

x_test = (x_test - x_train_mean) / x_train_standardization_deviation
y_test = (y_test - y_train_mean) / y_train_standardization_deviation

obs_matrix = np.hstack((np.ones(x_train.shape), x_train))

# TODO: calculate theta using Batch Gradient Descent
theta_best = np.random.rand(2, 1)
i_range = 100000
learning_rate = 0.0001
m = x_train.shape[0]

for i in range(int(i_range)):
    gradient_MSE = 2 / m * obs_matrix.T.dot(obs_matrix.dot(theta_best) - y_train)
    theta_best = theta_best - learning_rate * gradient_MSE

# TODO: calculate error
MSE = sum(((theta_best[0] + theta_best[1] * x_test) - y_test) ** 2) / len(x_test)
print(f'MSE: {MSE}, theta: {theta_best.flatten()}')

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0][0]) + float(theta_best[1][0]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()