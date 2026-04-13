

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, confusion_matrix


df = pd.read_excel("THROUGHPUT & CAPACITY STABILITY.xlsx")


df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Hour'] = df['Timestamp'].dt.hour


df['p10'] = (
    df.groupby(['Plant', 'Hour'])['ProductionUnits']
      .transform(lambda x: x.quantile(0.10))
)


df['LowOutputEvent'] = (df['ProductionUnits'] < df['p10']).astype(int)


features = [
    'EnergyConsumption',
    'Temperature',
    'Vibration',
    'Pressure'
]

X = df[features]
y = df['LowOutputEvent']


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


model = LogisticRegression(
    class_weight='balanced',   
    max_iter=1000              
)


model.fit(X_train, y_train)


y_pred = model.predict(X_test)


print("F1 Score:", f1_score(y_test, y_pred))


print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


print("Actual (first 10):", y_test.values[:10])
print("Predicted (first 10):", y_pred[:10])