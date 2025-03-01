document.getElementById('orderForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const orderId = document.getElementById('order_id').value;
    const location = document.getElementById('location').value;
    fetch('/api/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ order_id: orderId, location: location })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Delivery Date: ${data.delivery_date}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});