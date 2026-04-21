import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Load Dataset
data = pd.read_csv("animal_health_clean.csv")

X = data[['Age_Years',
          'Weight_kg',
          'Body_Temperature_F',
          'Behavior_Change',
          'Appetite_Change',
          'Vomiting']]

y = data['health_status']

model = DecisionTreeClassifier()
model.fit(X, y)

def predict_health(age, weight, temp, behavior, appetite, vomiting):
    result = model.predict([[age, weight, temp, behavior, appetite, vomiting]])
    if result[0] == 1:
        return "Unhealthy"
    else:
        return "Healthy"
