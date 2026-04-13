import pandas as pd
import numpy as np
from xgboost import XGBRegressor


df = pd.read_excel("THROUGHPUT & CAPACITY STABILITY.xlsx")

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Date'] = df['Timestamp'].dt.date


daily = df.groupby(['Plant', 'Date']).agg({
    'ProductionUnits': 'sum',
    'EnergyConsumption': 'sum',
    'MaintenanceFlag': 'sum',
    'DefectCount': 'sum'
}).reset_index()

daily['Date'] = pd.to_datetime(daily['Date'])


daily = daily.sort_values(['Plant', 'Date'])

daily['dayofweek'] = daily['Date'].dt.dayofweek
daily['month'] = daily['Date'].dt.month

# Lag features
daily['lag_1'] = daily.groupby('Plant')['ProductionUnits'].shift(1)
daily['lag_7'] = daily.groupby('Plant')['ProductionUnits'].shift(7)

daily = daily.dropna()


split_date = daily['Date'].max() - pd.Timedelta(days=14)

train = daily[daily['Date'] < split_date]
test = daily[daily['Date'] >= split_date]


baseline_preds = []

for plant in test['Plant'].unique():
    plant_train = train[train['Plant'] == plant]
    plant_test = test[test['Plant'] == plant]
    
    last_value = plant_train.iloc[-1]['ProductionUnits']
    preds = [last_value] * len(plant_test)
    baseline_preds.extend(preds)

test = test.copy()
test['Baseline_Pred'] = baseline_preds


features = [
    'dayofweek', 'month',
    'lag_1', 'lag_7',
    'EnergyConsumption',
    'MaintenanceFlag',
    'DefectCount'
]

model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

model.fit(train[features], train['ProductionUnits'])

test['ML_Pred'] = model.predict(test[features])


def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

baseline_mape = mape(test['ProductionUnits'], test['Baseline_Pred'])
ml_mape = mape(test['ProductionUnits'], test['ML_Pred'])

print("Baseline MAPE:", round(baseline_mape, 2))
print("Improved ML MAPE:", round(ml_mape, 2))


future_results = []

for plant in daily['Plant'].unique():
    plant_data = daily[daily['Plant'] == plant].copy()
    history = plant_data.copy()

    for i in range(14):
        next_date = history['Date'].max() + pd.Timedelta(days=1)
        
        lag_1 = history.iloc[-1]['ProductionUnits']
        lag_7 = history.iloc[-7]['ProductionUnits']
        
        # Use last known values for external features
        energy = history.iloc[-1]['EnergyConsumption']
        maint = history.iloc[-1]['MaintenanceFlag']
        defect = history.iloc[-1]['DefectCount']
        
        row = pd.DataFrame({
            'dayofweek': [next_date.dayofweek],
            'month': [next_date.month],
            'lag_1': [lag_1],
            'lag_7': [lag_7],
            'EnergyConsumption': [energy],
            'MaintenanceFlag': [maint],
            'DefectCount': [defect]
        })
        
        pred = model.predict(row)[0]
        
        new_row = pd.DataFrame({
            'Plant': [plant],
            'Date': [next_date],
            'ProductionUnits': [pred],
            'EnergyConsumption': [energy],
            'MaintenanceFlag': [maint],
            'DefectCount': [defect]
        })
        
        history = pd.concat([history, new_row], ignore_index=True)
        
        future_results.append({
            'Plant': plant,
            'Date': next_date,
            'Forecast': pred
        })

future_df = pd.DataFrame(future_results)

print("\nFuture Forecast:")
print(future_df.head())


future_df.to_excel("forecast_output.xlsx", index=False)