import pickle
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

# Load historical delivery data
data = pd.read_csv('historical_delivery_data.csv')

# Features: order day, distance, local hub performance
X = data[['order_day', 'distance', 'local_hub_performance']].values
# Target: delivery days
y = data['delivery_days'].values

# Train the model
model = RandomForestRegressor()
model.fit(X, y)

# Save the model to a file
with open('delivery_model.pkl', 'wb') as file:
    pickle.dump(model, file)