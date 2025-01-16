# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Example data
data = {
    'Age': [29, 45, 50, 39, 48, 50, 55, 60, 62, 43],
    'Cholesterol': [220, 250, 230, 180, 240, 290, 310, 275, 300, 280],
    'Max_Heart_Rate': [180, 165, 170, 190, 155, 160, 150, 140, 130, 148],
    'Heart_Disease': [0, 1, 1, 0, 1, 1, 1, 1, 1, 0]
}
df = pd.DataFrame(data)

# Independent variables (features) and dependent variable (target)
X = df[['Age', 'Cholesterol', 'Max_Heart_Rate']]
y = df['Heart_Disease']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Creating and training the random forest model
model = RandomForestClassifier(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print(f"Confusion Matrix:\n{conf_matrix}")
print(f"Classification Report:\n{class_report}")

# Feature importance
feature_importances = pd.DataFrame(model.feature_importances_, index=X.columns, columns=['Importance']).sort_values('Importance', ascending=False)
print(f"Feature Importances:\n{feature_importances}")

# Plotting the feature importances
sns.barplot(x=feature_importances.index, y=feature_importances['Importance'])
plt.title('Feature Importances')
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.show()