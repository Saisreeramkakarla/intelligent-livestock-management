import pandas as pd

# Load dataset
data = pd.read_csv("animal_health_clean.csv")

print("\n---- MULTI-FACTOR COMBINATION ANALYSIS ----")

# Case 1: High Temp + Vomiting
combo1 = data[(data['Body_Temperature_F'] > 102) & (data['Vomiting'] == 1)]
print("\nHigh Temperature + Vomiting:")
print(combo1['health_status'].value_counts())

# Case 2: High Temp + Behavior Change
combo2 = data[(data['Body_Temperature_F'] > 102) & (data['Behavior_Change'] == 1)]
print("\nHigh Temperature + Behavior Change:")
print(combo2['health_status'].value_counts())

# Case 3: Vomiting + Appetite Change
combo3 = data[(data['Vomiting'] == 1) & (data['Appetite_Change'] == 1)]
print("\nVomiting + Appetite Change:")
print(combo3['health_status'].value_counts())

# Case 4: All three combined
combo4 = data[(data['Body_Temperature_F'] > 102) &
              (data['Vomiting'] == 1) &
              (data['Behavior_Change'] == 1)]

print("\nHigh Temp + Vomiting + Behavior Change:")
print(combo4['health_status'].value_counts())
