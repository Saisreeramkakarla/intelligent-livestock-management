import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("animal_health_clean.csv")

X = data[['Age_Years',
          'Weight_kg',
          'Body_Temperature_F',
          'Behavior_Change',
          'Appetite_Change',
          'Vomiting']]

y = data['health_status']

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Models
lr = LogisticRegression(max_iter=1000)
dt = DecisionTreeClassifier()
rf = RandomForestClassifier()

lr.fit(X_train, y_train)
dt.fit(X_train, y_train)
rf.fit(X_train, y_train)

lr_acc = accuracy_score(y_test, lr.predict(X_test))
dt_acc = accuracy_score(y_test, dt.predict(X_test))
rf_acc = accuracy_score(y_test, rf.predict(X_test))

print("Logistic Regression Accuracy:", lr_acc)
print("Decision Tree Accuracy:", dt_acc)
print("Random Forest Accuracy:", rf_acc)

best_model = rf   # based on accuracy

# ---------------------
# Prediction Function
# ---------------------

def predict_health_and_disease(values):
    result = best_model.predict([values])[0]

    if result == 0:
        return "Healthy", "None"

    # Disease rules
    temp = values[2]
    vomiting = values[5]
    appetite = values[4]
    behavior = values[3]

    if temp > 103:
        return "Unhealthy", "Fever"
    elif vomiting == 1:
        return "Unhealthy", "Digestive Disorder"
    elif behavior == 1:
        return "Unhealthy", "Respiratory Infection"
    elif appetite == 1:
        return "Unhealthy", "Nutritional Deficiency"
    else:
        return "Unhealthy", "General Infection"
