# Importing the required libraries
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression

import random
import os

def graph(y_test_last, y_pred_last, Pos_Filter):
  # Plot the frequencies
  plt.figure(figsize=(18, 6))
  plt.plot(y_test_last, color='skyblue')
  plt.plot(y_pred_last, color='red')
  plt.xlabel('Draw')
  plt.ylabel('Skip_value')
  plt.title(str(Pos_Filter) + ' vs. ' +str(EMA) + 'Prediction')
  #plt.xticks(range(min(numbers), max(numbers) + 1))
  plt.grid()
  plt.show()
  return

def addTomorrow(df_partial, Pos_Filter):
  # Calculate if tomorrow value is greater than (1) median
  df_partial['target'] = df_partial[Pos_Filter].shift(-1)
  data = df_partial.iloc[:-1]
  return data

def split_train(X, y):
  # Split the data into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
  # Train a Random Forest model
  rf.fit(X_train, y_train)
  return X_test, y_test

def just_train(rf, X, y):
  # Train a Random Forest model
  rf.fit(X, y)
  return

def just_train_logistic(log_reg, X, y):
  # Train a Random Forest model
  log_reg.fit(X, y)
  return

def logistic_split_train(X, y):
  # Split the dataset into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
  # Train Logistic Regressor model
  log_reg.fit(X_train, y_train)
  return X_test, y_test

def prep_to_graph(df_summary, EMA):
  y_test_last = df_summary[Pos_Filter][-20:]
  y_pred_last = df_summary[EMA][-20:]
  return y_test_last, y_pred_last

def generate_random_numbers(df, df_partial, Pos_Filter, number_of_rows, number_of_rows_reduced):
  # Fill 'random' column with random skips and evaluate the correlation between Pos_Filter and 'random'. Exit when correlation > 0.3
  #while not correlation > 0.2 or correlation < -0.2:
  for i in range(number_of_rows_reduced, 0, -1):
    row = random.randint(0, number_of_rows - 1)
    df_partial.loc[number_of_rows - i, 'random'] = df.loc[row, Pos_Filter]
  return df_partial

# csv Master File
df = pd.read_csv(r'/Users/gustavo.vaca/Downloads/daily4night - Sheet24.csv')

# csv for Pos_isEven1
# csv for Pos_isEven2
# csv for Pos_isEven3
# csv for Pos_isEven4

# csv for Pos_highLow1
# csv for Pos_highLow2
# csv for Pos_highLow3
# csv for Pos_highLow4

# csv for Pos_Layout1
# csv for Pos_Layout2
# csv for Pos_Layout3
# csv for Pos_Layout4

# Set Filter
Pos_Filter = 'Pos_Layout4'
rowsToCheck = 20

# Clear the screen terminal and Calculate Pos_Filter median
os.system('clear')

median = df[Pos_Filter].median().astype(int)
print('Median = ' + str(df[Pos_Filter].median().astype(int)) + '\n')
print('Mean = ' + str(df[Pos_Filter].mean().astype(int)) + '\n')
print('Standard Deviation = ' + str(df[Pos_Filter].std()) + '\n')

# Define RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
# Define Logistic Regressor model
#log_reg = LogisticRegression(C=0.0001, max_iter=1000, penalty='none', solver='saga', random_state=0)
log_reg = LogisticRegression()

predictors = [Pos_Filter]
df_partial = df[predictors][-20:]
# 153 for Posn (median = 5). 129 for Skip_Pos1 and Skip_Pos4 (median = 6)

number_of_rows = len(df)
number_of_rows_reduced = len(df_partial)

# Pre random generation
for i in range(10000000):
  row = random.randint(0, number_of_rows - 1)

correlation = 0
correlation1 = 0
count =0
while not correlation1 >= 0.65 or correlation1 <= -0.65: # +/- 0.60
  #while not correlation >= 0.98 or correlation <= -0.98: # +/- 0.96
  count += 1

  df_partial = generate_random_numbers(df, df_partial, Pos_Filter, number_of_rows, number_of_rows_reduced)

  predictors = [Pos_Filter, 'random']
  data = addTomorrow(df_partial, Pos_Filter)

  X = data[predictors]
  y = data[['target']]
  just_train_logistic(log_reg, X, y)

  # Make predictions
  y_pred = log_reg.predict(X).astype(int)

  df_summary = y.astype(int)
  df_summary.rename(columns={'target': Pos_Filter}, inplace=True)
  EMA = 'Skip '
  df_summary[EMA] = y_pred

  #correlation = df_summary.iloc[-rowsToCheck:][Pos_Filter].corr(df_summary.iloc[-rowsToCheck:][EMA])
  correlation1 = df_summary[Pos_Filter].corr(df_summary[EMA])

print(count)

# List the features used to predict the future value
df_to_predict = df_partial[predictors]

# Predict future value
result = log_reg.predict(df_to_predict.iloc[-1:]).astype(int)
skip_prediction = result

y_test_last, y_pred_last = prep_to_graph(df_summary, EMA)

graph(y_test_last, y_pred_last, Pos_Filter)

df_summary['up/down'] = (df_summary[Pos_Filter] <= df_summary[EMA]).astype(int)

# Calculate %
print(str(Pos_Filter) + ' (predicted) is less than or equal to  ' + str(EMA) + ' (%)')
print(df_summary['up/down'].value_counts()*100/df_summary['up/down'].count())

df_summary['up/down'] = (df_summary[Pos_Filter] >= df_summary[EMA]).astype(int)

# Calculate %
print(str(Pos_Filter) + ' (predicted) is greater than or equal to ' + str(EMA) + ' (%)')
print(df_summary['up/down'].value_counts()*100/df_summary['up/down'].count())

df_summary['up/down'] = (df_summary[Pos_Filter] == df_summary[EMA]).astype(int)

# Calculate %
print(str(Pos_Filter) + ' (predicted) is equal to ' + str(EMA) + ' (%)')
print(df_summary['up/down'].value_counts()*100/df_summary['up/down'].count())

df_summary['delta'] = abs(df_summary[Pos_Filter] - df_summary[EMA])
df_summary['delta_net'] = df_summary[Pos_Filter] - df_summary[EMA]

# Calculate delta mean and standard deviation
residual_mean = df_summary['delta'].mean()
residual_std = df_summary['delta'].std()
residual_mean_net = df_summary['delta_net'].mean()
residual_std_net = df_summary['delta_net'].std()

# Calculate the 20th percentile
percentile_20 = round(df_summary['delta'].quantile(0.20))
percentile_20_net = round(df_summary['delta_net'].quantile(0.20))

# Calculate the 80th percentile
percentile_80 = round(df_summary['delta'].quantile(0.80))
percentile_80_net = round(df_summary['delta_net'].quantile(0.80))

# Calculate the min and max
residual_min = df_summary['delta'].min()
residual_max = df_summary['delta'].max()

residual_min_net = df_summary['delta_net'].min()
residual_max_net = df_summary['delta_net'].max()

print('Correlation between ' + str(Pos_Filter) + ' and random skip before prediction = ' + str(df_partial[Pos_Filter].corr(df_partial['random'])))
print('Correlation between ' + str(Pos_Filter) + ' and random skip for predictions = ' + str(df_summary[Pos_Filter].corr(df_summary[EMA])))
print('Correlation between ' + str(Pos_Filter) + ' and random skip for last ' +str(rowsToCheck) + ' predictions = ' + str(df_summary.iloc[-rowsToCheck:][Pos_Filter].corr(df_summary.iloc[-rowsToCheck:][EMA])) + '\n')
print(str(Pos_Filter) + ' last value = ' + str(df_to_predict.iloc[-1:][Pos_Filter].values[0]))
print(str(Pos_Filter) + ' last predicted value = ' + str(df_summary.iloc[-1:][EMA].values[0]))
print(str(Pos_Filter) + ' prediction = ' + str(skip_prediction) + '\n')

print('delta mean ' + str(residual_mean))
print('delta std ' + str(residual_std))
print('delta mean + delta std = ' + str(residual_mean + residual_std))
print('delta min ' + str(residual_min))
print('delta max ' + str(residual_max) + '\n')

print('delta mean net ' + str(residual_mean_net))
print('delta std net ' + str(residual_std_net) + '\n')

print('20th percentile ' + str(percentile_20))
print('80th percentile ' + str(percentile_80))
print('20th percentile_net ' + str(percentile_20_net))
print('80th percentile_net ' + str(percentile_80_net))
#print(Pos_Filter + ' would be between ' + str(skip_prediction + percentile_20) + ' and ' + str(skip_prediction + percentile_80))

# Calculate % accuracy up/down prediction
df_summary['tempo1'] = (df_summary[Pos_Filter].shift(-1) > df_summary[Pos_Filter]).astype(int)
df_summary['tempo2'] = (df_summary[EMA].shift(-1) > df_summary[EMA]).astype(int)

# Create 'conteo' column before assigning values
df_summary['conteo'] = 0  # Initialize the column with zeros

# Check if current and predicted values are equal and set 'conteo' accordingly
df_summary['conteo'] = (df_summary['tempo1'] == df_summary['tempo2']).astype(int)

# Print percentage of 1s and 0s in 'conteo'
conteo_counts = df_summary['conteo'].value_counts(normalize=True) * 100
print(conteo_counts)

# Take df and calculate 20% and 80% Pos_Filter delta percentile
df['tempo3'] = abs(df[Pos_Filter].shift(-1) - df[Pos_Filter])
# Calculate the 20th percentile
percentile_20_Pos = round(df['tempo3'].quantile(0.125))
# Calculate the 80th percentile
percentile_80_Pos = round(df['tempo3'].quantile(0.875))

print('Delta filter value should be between ' + str(percentile_20_Pos) + ' and ' + str(percentile_80_Pos) + ' (75% accuracy)')

# Considerar este valor cuando valor predicho es igual al ultimo predicho y filtro vs. skip es alto (>=30%)
#(df_summary['delta'].value_counts()[0] + df_summary['delta'].value_counts()[1] + df_summary['delta'].value_counts()[2])*100/len(df_summary)
(df_summary['delta'].value_counts()[0])*100/len(df_summary)

# Analisis: 
# Observar coincidencias entre Pos predicted (less, greather, equal) and predicted value