

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score


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


model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
)

model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print("F1 Score:", f1_score(y_test, y_pred))
print("Actual:", y_test.values[:10])
print("Predicted:", y_pred[:10])
