
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bingo.symbolic_regression.symbolic_regressor import SymbolicRegressor

regressor = SymbolicRegressor(population_size=500, stack_size=16, operators = {"+", "-", "*"},
                              use_simplification=False, generations=100000, 
                              fitness_threshold=1E-3, max_time=90, max_evals=100000,
                              clo_threshold=1E-3, scale_max_evals=False)

#filepath and name
training_file = "/Users/clarissaseebohm/Desktop/ME EN 5510/Project/cs-ap/data/training_data_50/training_data.csv"

#read csv using pandas 
df_ = pd.read_csv(training_file)
df = df_.sort_values(by='Radius', axis=0)
df = df.drop(labels=13, axis=0)
df = df.drop(labels=38, axis=0)


x = df['Radius'].to_numpy().reshape([-1, 1])
y = df['MaxStress'].to_numpy()

#fitting the regressor
regressor.fit(x, y)

#finding the best individual
best_individual = regressor.get_best_individual()
print("best individual is:", best_individual)


#predicting data with the best individual
x_linear = np.linspace(1,99,30).reshape([-1, 1])
pred_y = best_individual.evaluate_equation_at(x_linear)

#plot the best individual
plt.scatter(x, y)
plt.plot(x_linear, pred_y, "r")
plt.xlabel("Radius")
plt.ylabel("Max Stress")
plt.legend(["Abaqus Data", "Bingo Prediction", "Infinite Plate Solution"])
plt.show()

"ANALYSIS"
#filepath and name
validation_file = "/Users/clarissaseebohm/Desktop/ME EN 5510/Project/cs-ap/data/validation_data/validation_data.csv"

#read validation csv using pandas 
dfv_ = pd.read_csv(validation_file)
dfv = dfv_.sort_values(by='Radius', axis=0)

x_v = dfv['Radius'].to_numpy().reshape([-1, 1])
y_v = dfv['MaxStress'].to_numpy()

#infinite plate solution
y3 = np.zeros(x_linear.size)
y3.fill(3.0E6)

#plot the best individual
plt.scatter(x, y)
plt.scatter(x_v, y_v)
plt.plot(x_linear, pred_y, "r")
plt.plot(x_linear, y3, "y")
plt.title("Radius vs Max Stress (Sample Size - 50)")
plt.xlabel("Radius")
plt.ylabel("Max Stress")
plt.legend(["Abaqus Training Data", "Abaqus Validation Data", "Bingo Prediction", "Infinite Plate Solution"])
plt.show()