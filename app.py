from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import datetime
from flask_cors import CORS
from geopy.distance import geodesic
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

# Define Order model to track past orders
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Load the trained Random Forest model
model_path = os.path.join(os.getcwd(), 'delivery_model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Function to calculate distance
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

# Function to determine local hub
local_hubs = [
    {'name': 'Mumbai Hub', 'latitude': 19.0760, 'longitude': 72.8777},
    {'name': 'Bangalore Hub', 'latitude': 12.9716, 'longitude': 77.5946},
    {'name': 'Kolkata Hub', 'latitude': 22.5726, 'longitude': 88.3639},
]

def find_nearest_hub(user_lat, user_lon):
    return min(local_hubs, key=lambda hub: calculate_distance(user_lat, user_lon, hub['latitude'], hub['longitude']))

# Function to get order frequency at a location
def get_order_frequency(user_lat, user_lon):
    recent_orders = Order.query.filter(Order.latitude == user_lat, Order.longitude == user_lon).count()
    return recent_orders

# Function to generate available delivery dates
def get_available_dates(predicted_date, order_frequency):
    if order_frequency > 10:
        gap = 1
    elif order_frequency > 5:
        gap = 2
    else:
        gap = 4
    return [(predicted_date + datetime.timedelta(days=i * gap)).strftime("%Y-%m-%d") for i in range(1, 5)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        user_location = data.get('user_location')
        use_central_hub = data.get('use_central_hub', True)
        
        if not user_location:
            return jsonify({'error': 'Missing location data'}), 400
        
        if use_central_hub:
            hub_latitude, hub_longitude = 28.6139, 77.2090  # Latitude and Longitude of New Delhi, India
        else:
            nearest_hub = find_nearest_hub(user_location['latitude'], user_location['longitude'])
            hub_latitude, hub_longitude = nearest_hub['latitude'], nearest_hub['longitude']
        
        distance = calculate_distance(hub_latitude, hub_longitude, user_location['latitude'], user_location['longitude'])
        order_frequency = get_order_frequency(user_location['latitude'], user_location['longitude'])
        
        input_features = np.array([[distance, order_frequency]])
        predicted_days = model.predict(input_features)[0]
        predicted_date = datetime.datetime.now() + datetime.timedelta(days=int(predicted_days))
        available_dates = get_available_dates(predicted_date, order_frequency)
        
        return jsonify({'predicted_date': predicted_date.strftime("%Y-%m-%d"), 'available_dates': available_dates})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)