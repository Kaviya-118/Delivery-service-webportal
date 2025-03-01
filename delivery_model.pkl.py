import pickle
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Example data for training
X = np.array([[i, np.random.uniform(1, 100)] for i in range(1, 31)])  # Features: order day, distance
y = np.array([i + np.random.randint(1, 5) for i in range(1, 31)])  # Output value: delivery day with some randomness

# Train the model
model = RandomForestRegressor()
model.fit(X, y)

# Save the model to a file
with open('delivery_model.pkl', 'wb') as file:
    pickle.dump(model, file)