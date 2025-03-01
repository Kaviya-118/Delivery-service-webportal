import React, { useState } from "react";

export default function App() {
    const [orderId, setOrderId] = useState("");
    const [prediction, setPrediction] = useState(null);

    const getUserLocationAndPredict = async () => {
        if (!orderId) {
            alert("Enter Order ID.");
            return;
        }

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    console.log("User location:", latitude, longitude);  // Debugging

                    const response = await fetch("http://127.0.0.1:5000/predict", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            order_id: orderId,
                            latitude: latitude,
                            longitude: longitude,
                        }),
                    });

                    console.log("Fetch response:", response);  // Debugging

                    if (!response.ok) {
                        alert("Error: " + response.statusText);
                        return;
                    }

                    const data = await response.json();
                    console.log("Prediction data:", data);  // Debugging
                    setPrediction(data);
                },
                (error) => {
                    console.error("Geolocation error:", error);  // Debugging
                    alert("Location access denied!");
                }
            );
        } else {
            alert("Geolocation not supported.");
        }
    };

    return (
        <div className="container">
            <h1>Parcel Delivery Prediction</h1>
            <input
                type="text"
                placeholder="Enter Order ID"
                value={orderId}
                onChange={(e) => setOrderId(e.target.value)}
            />
            <button onClick={getUserLocationAndPredict}>Predict Delivery Date</button>
            {prediction && (
                <div>
                    <h2>Predicted Delivery Date: {prediction.predicted_date}</h2>
                    <h3>Available Dates:</h3>
                    <ul>
                        {prediction.available_dates.map((date, index) => (
                            <li key={index}>{date}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}