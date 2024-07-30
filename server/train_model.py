import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import xgboost as xgb

data = pd.read_csv('C:/Users/dhari/Desktop/IOT_Automatic_Irrigation/data/sensor_data.csv')
data.replace(to_replace = {'nan':0},inplace=True)
data.replace(to_replace = {'OFF':0,'ON':1},inplace=True)

y = data['Status']
X = data.drop(['Status','Time'], axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create XGBoost model
model = xgb.XGBClassifier()

# Train the model
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# Save the model
joblib.dump(model, 'soil_moisture_model.pkl')
