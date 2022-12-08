import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import math as m

def bingo(x):
    y = (9.342098563231744*10**(-17))*(x**12) + (0.163519)*(x**4) + (0.163519)*(x**2) + 2794027.683846
    return y

#FIND RMSE FOR TRAINING DATA
#filepath and name
training_file = "/Users/clarissaseebohm/Desktop/ME EN 5510/Project/cs-ap/data/training_data_50/training_data.csv"

#read csv using pandas 
df_ = pd.read_csv(training_file)
df = df_.sort_values(by='Radius', axis=0)

#drop data points with radius within 5% of the edge
df = df.drop(labels=13, axis=0)
df = df.drop(labels=38, axis=0)

x = df['Radius'].to_numpy().reshape([-1, 1])
y = df['MaxStress'].to_numpy()

pred_y_training = bingo(x)

rsme_training = m.sqrt(mean_squared_error(y, pred_y_training))

print(rsme_training)

#FIND RMSE FOR VALIDATION DATA
#filepath and name
validation_file = "/Users/clarissaseebohm/Desktop/ME EN 5510/Project/cs-ap/data/validation_data/validation_data.csv"

#read validation csv using pandas 
dfv_ = pd.read_csv(validation_file)
dfv = dfv_.sort_values(by='Radius', axis=0)

x_v = dfv['Radius'].to_numpy().reshape([-1, 1])
y_v = dfv['MaxStress'].to_numpy()

pred_y_v = bingo(x_v)

rsme_v = m.sqrt(mean_squared_error(y_v, pred_y_v))

print(rsme_v)

"""
#CHECK EQUATION
x_linear = np.linspace(1,99,30).reshape([-1, 1])
pred_y = bingo(x_linear)

print(pred_y)

#plot the best individual
plt.scatter(x, y)
plt.plot(x_linear, pred_y, 'r')
plt.title("Abaqus Training Data and Bingo Prediction (Sample Size = 50)")
plt.xlabel("Radius [mm]")
plt.ylabel("Max Stress [Pa]")
plt.legend(["Abaqus Training Data", "Bingo Prediction"])
plt.show()
"""